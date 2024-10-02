from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.models import Lawyer, QueryRequest
from app.services.service import url_to_img, byte_to_img
from app.core.database import get_db
from app.services.langchain import prompt, rag
from app.services.langchain.prompt import run_chain
from deepface import DeepFace
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings
from sqlalchemy import text
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
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

class Settings(BaseSettings):
    authjwt_secret_key: str = os.getenv("SECRET_KEY")

@AuthJWT.load_config
def get_config():
    return Settings()

@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decoded_token):
    return False  

# DB Update Query
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
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()  
    except KeyError as e:
        if 'type' not in str(e):
            raise e  

    user_email = Authorize.get_raw_jwt().get('username') 
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

@router.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    logger.info(f"Received request to analyze video with file: {file.filename}")

    try:
        file_content = await file.read()
        logger.info(f"File size: {len(file_content)} bytes")

        result = {
            "aiRelatedInformation": "Sample AI Information",
            "aiRelatedLaw": "Sample AI Law",
            "aiUserFault": 80,
            "aiOtherFault": 20
        }
        
        logger.info(f"Returning result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Error processing video file")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.post("/api/v1/search-query")
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):

    query_text = request.query_text
    accident_location = request.accident_location
    a_direction = request.a_direction
    b_direction = request.b_direction
    a_percentage = request.a_percentage
    b_percentage = request.b_percentage
    accident_location_description = request.accident_location_description

    embedding_function = OpenAIEmbeddings(openai_api_key= os.getenv("SECRET_KEY"))  
    vector_store = Chroma(persist_directory="chroma_data", embedding_function=embedding_function)

    try:
        similar_queries = vector_store.similarity_search(query_text, k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail="유사한 쿼리를 검색하는 중 오류가 발생했습니다.")

    results = []

    for similar_query in similar_queries:
        try:
            # `run_chain()`을 사용하여 사고 정보 분석 및 결과 얻기
            result = run_chain(
                accident_location=accident_location,
                a_direction=a_direction,
                b_direction=b_direction,
                a_percentage=a_percentage,
                b_percentage=b_percentage,
                accident_location_description=accident_location_description
            )
            results.append(result)

        except Exception as e:
            raise HTTPException(status_code=500, detail="프롬프트 처리 중 오류가 발생했습니다.")

        return JSONResponse(content={"similar_terms_results": [result.dict() for result in results]})