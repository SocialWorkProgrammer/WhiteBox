import httpx
import re
import os
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.models import Lawyer, QueryRequest
from app.services.service import url_to_img, byte_to_img
from app.core.database import get_db
from app.services.langchain import prompt, rag
from app.services.langchain.prompt import run_chain
from deepface import DeepFace
from pydantic import BaseModel
from sqlalchemy import text
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

METRICS = ["cosine", "euclidean", "euclidean_12"]
DISTANCE_THRESHOLD = 0.3
SUCCESS_MESSAGE = "변호사 인증 성공!"
FAILURE_MESSAGE = "변호사 인증 실패"
USER_TYPE_LAWYER = "LAWYER"
USER_TYPE_MEMBER = "MEMBER"

class User(BaseModel):
    username: str
    email: str

def update_user_type_to_lawyer(db: Session, user_email: str):
    db.execute(
        text("UPDATE user SET user_type = :user_type WHERE user_email = :user_email"),
        {"user_type": USER_TYPE_LAWYER, "user_email": user_email}
    )
    db.commit()

def verify_lawyer_image(lawyer_image_url: str, uploaded_image_bytes: bytes):
    lawyer_image = url_to_img(lawyer_image_url)
    uploaded_image = byte_to_img(uploaded_image_bytes)
    return DeepFace.verify(img1_path=lawyer_image, img2_path=uploaded_image)

@router.post("/api/v1/lawyer")
async def compare_image(
    name: str, 
    date: str, 
    user_email: str,
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_name == name, Lawyer.lawyer_date == date).first()

    if not lawyer:
        raise HTTPException(status_code=404, detail=FAILURE_MESSAGE)

    uploaded_image_bytes = await file.read()
    result = verify_lawyer_image(lawyer.lawyer_image_url, uploaded_image_bytes)
    distance = result['distance']

    if distance <= DISTANCE_THRESHOLD:
        update_user_type_to_lawyer(db, user_email)
        return JSONResponse(content={"message": SUCCESS_MESSAGE, "user_type": USER_TYPE_LAWYER})
    
    return JSONResponse(content={"message": FAILURE_MESSAGE, "user_type": USER_TYPE_MEMBER})



@router.post("/api/v1/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    logger.info(f"Received request to analyze video with file: {file.filename}")

    try:
        file_content = await file.read()
        logger.info(f"File size: {len(file_content)} bytes")
        # 이 더미데이터를 채워서 return 해주면 됩니다!~@!@~!@~!@@@!~!~!~!~!~!~
        result = {
            "aiDescription": "사고 발생 상황 분석",
            "aiExplanation": "과실 비율과 그 근거",
            "aiResult": "법적 기준 및 결론",
            "aiRelatedLaw": "관련 법(있을수도있고없을수도있음)",
            "aiUserFault": 80,
            "aiOtherFault": 20
        }
        
        logger.info(f"Returning result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Error processing video file")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")



# LLM 
 
@router.post("/api/v1/search-query")
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):

    query_text = request.query_text 
    accident_location = request.accident_location
    accident_location_description = request.accident_location_description
    a_direction = request.a_direction
    b_direction = request.b_direction
    a_percentage = request.a_percentage
    b_percentage = request.b_percentage

    embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))  
    vector_store = Chroma(persist_directory="chroma_data", embedding_function=embedding_function)

    try:
        similar_query = vector_store.similarity_search(query_text, k=1)
        if not similar_query:
            raise HTTPException(status_code=404, detail="유사한 쿼리를 찾을 수 없습니다.")
        
        retrieved_content = similar_query[0].page_content
        match = re.search(r'\\(\d+)', retrieved_content)
        if not match:
            raise HTTPException(status_code=500, detail="검색된 쿼리에서 번호를 추출할 수 없습니다.")
        
        case_number = match.group(1)
    except Exception as e:
        raise HTTPException(status_code=500, detail="유사한 쿼리를 검색하는 중 오류가 발생했습니다.")

    # 번호에 해당하는 파일 내용을 읽기 위한 폴더 목록
    folder_paths = [
        "참조판례", "판례내용"
    ]
    
    base_path = "판례" 

    case_details = {}
    reference_case_content = None
    precedent_content = None
    try:
        for folder in folder_paths:
            file_path = os.path.join(base_path, folder, f"{case_number}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='euc-kr') as file:
                    if folder == "참조판례":
                        reference_case_content = file.read()  
                    elif folder == "판례내용":
                        precedent_content = file.read() 
            else:
                if folder == "참조판례":
                    reference_case_content = f"{folder}에서 {case_number}에 해당하는 파일을 찾을 수 없습니다."
                elif folder == "판례내용":
                    precedent_content = f"{folder}에서 {case_number}에 해당하는 파일을 찾을 수 없습니다."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"케이스 내용을 읽는 중 오류가 발생했습니다: {str(e)}")


    results = []
    try:
        if precedent_content:
            result = run_chain(
                accident_location=accident_location,
                accident_location_description=accident_location_description,
                a_direction=a_direction,
                b_direction=b_direction,
                a_percentage=a_percentage,
                b_percentage=b_percentage,
                precedent_content=precedent_content  
            )
            results.append(result)
        else:
            raise HTTPException(status_code=500, detail="판례내용이 없습니다. 프롬프트를 실행할 수 없습니다.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="프롬프트 처리 중 오류가 발생했습니다.")

    response_data = {
            "reference_case": reference_case_content,
            "results": results
        }

    try:
        async with httpx.AsyncClient() as client:
            spring_response = await client.post(
                "http://localhost/api/v1/upload-video",  
                json=response_data
            )
            spring_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Spring 서버로 전송 중 오류가 발생했습니다: {str(e)}")

    return JSONResponse(content=response_data)