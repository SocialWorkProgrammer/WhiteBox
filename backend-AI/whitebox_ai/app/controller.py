import httpx
import re
import os
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.models import QueryRequest
from app.services.service import url_to_img, byte_to_img
from app.core.database import get_db
from app.services.langchain.prompt import run_chain
from deepface import DeepFace
from pydantic import BaseModel
from sqlalchemy import text
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import logging

import traceback
import cv2
import torch
from mmengine import Config
from mmdet.apis import inference_detector, init_detector
import tempfile
import shutil
from tqdm import tqdm
import subprocess
import pickle
import json

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
    img_path: str = Form(...),
    file: UploadFile = File(...)
):
    uploaded_image_bytes = await file.read()
    result = verify_lawyer_image(img_path, uploaded_image_bytes)
    distance = result['distance']

    if distance <= DISTANCE_THRESHOLD:
        return JSONResponse(content={"message": SUCCESS_MESSAGE, "user_type": USER_TYPE_LAWYER})
    
    return JSONResponse(content={"message": FAILURE_MESSAGE, "user_type": USER_TYPE_MEMBER})




def draw_predictions(image, bboxes, labels, class_names):
    no_bbox_classes = ["two-wheeled-vehicle", "pedestrian", "crosswalk", "bike"]
    color_map = {
        "traffic-light-red": (0, 0, 255),
        "traffic-light-green": (0, 255, 0),
        "vehicle": (255, 0, 0),
        "traffic-light-etc": (0, 255, 255),
        "traffic-sign": (255, 0, 255)
    }

    for bbox, label in zip(bboxes, labels):
        class_name = class_names[label]
        if class_name in no_bbox_classes:
            continue
        xmin, ymin, xmax, ymax = map(int, bbox)
        color = color_map.get(class_name, (255, 255, 255))
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)

    return image

def process_frame(model, frame, class_names):
    result = inference_detector(model, frame)
    labels = list(result.pred_instances.labels.cpu().numpy())
    bboxes = list(result.pred_instances.bboxes.cpu().numpy())
    frame_with_preds = draw_predictions(frame.copy(), bboxes, labels, class_names)
    return frame_with_preds

def run_mmaction2_inference():
    cmd = [
        "C:/Users/SSAFY/Desktop/ai test/venv/Scripts/python.exe", "C:/Users/SSAFY/Desktop/ai test/mmaction2/tools/test.py",
        "C:/Users/SSAFY/Downloads/slowfast_exp3.py",
        "C:/Users/SSAFY/Downloads/best_acc_top1_epoch_94.pth",
        "--work-dir", "C:/Users/SSAFY/Desktop/ai test/workspace"
    ]
    subprocess.run(cmd, check=True)


def load_classification_results():
    with open("C:/Users/SSAFY/Desktop/ai test/workspace/result.pkl", 'rb') as f:
        results = pickle.load(f)
    return results



@router.post("/api/v1/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    detection_config_path = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/cascade_rcnn_cfg.py"
    detection_checkpoint_path = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/best_coco_bbox_mAP_epoch_10.pth"

    temp_dir = tempfile.mkdtemp()
    temp_video_path = None
    output_dir = os.path.expanduser("C:/Users/SSAFY/Desktop/ai test/workspace/images")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 업로드된 비디오를 임시 파일로 저장
        temp_video_fd, temp_video_path = tempfile.mkstemp(suffix='.mp4')
        with os.fdopen(temp_video_fd, 'wb') as temp_file:
            temp_file.write(await file.read())

        print(f"Temporary video saved at: {temp_video_path}")

        # CPU 설정
        device = torch.device("cpu")
        # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        # 모델 초기화
        cfg = Config.fromfile(detection_config_path)
        model = init_detector(cfg, detection_checkpoint_path, device=device)
        class_names = model.dataset_meta['classes']
        print("Model initialized successfully")



        #################################################################

        # # 비디오 파일 열기
        # cap = cv2.VideoCapture(temp_video_path)
        # if not cap.isOpened():
        #     raise Exception("Error opening video file")

        # # 비디오 속성 가져오기
        # fps = int(cap.get(cv2.CAP_PROP_FPS))
        # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # print(f"Video FPS: {fps}, Total frames: {total_frames}")

        # frame_count = 0
        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         break

        #     # 프레임 리사이즈
        #     height, width = frame.shape[:2]
        #     new_width = 640
        #     new_height = int(height * (new_width / width))
        #     resized_frame = cv2.resize(frame, (new_width, new_height))

        #     # Bounding box 그리기
        #     frame_with_boxes = process_frame(model, resized_frame, class_names)

        #     # 결과 저장
        #     output_path = os.path.join(output_dir, f"img_{frame_count + 1:05d}.jpg")
        #     success = cv2.imwrite(output_path, frame_with_boxes)
        #     if not success:
        #         print(f"Failed to save image: {output_path}")
        #     else:
        #         print(f"Saved image: {output_path}")

        #     frame_count += 1

        # cap.release()

        # print(f"Total frames processed: {frame_count}")
        # print(f"Output directory: {output_dir}")

        # annotation_path = "C:/Users/SSAFY/Desktop/ai test/workspace/annotation.txt"
        # with open(annotation_path, 'w') as f:
        #     f.write(f"images {frame_count}")

        #################################################################


        run_mmaction2_inference()

        classification_results = load_classification_results()
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')

        # JSON 파일에서 dict_label 읽기
        with open("C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/dict_label.json", 'r', encoding='utf-8') as f:
            dict_label = json.load(f)
        ai_result = dict_label[str(classification_results[0]['pred_label'].item())]
        print(ai_result)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        
        # LLM
        query_text = f'{ai_result[0]} {ai_result[1]} {ai_result[2]} {ai_result[3]}'
        accident_location = ai_result[0]
        accident_location_description = ai_result[1]
        a_direction = ai_result[2]
        b_direction = ai_result[3]
        a_percentage = ai_result[4]
        b_percentage = ai_result[5]

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


        print('#############################')
        print('#############################')
        print('#############################')
        print(results)
        print('#############################')
        print('#############################')
        print('#############################')
        print(reference_case_content)
        print('#############################')
        print('#############################')
        print('#############################')

        aiRelatedLaw = reference_case_content
        if '해당하는 파일을 찾을 수 없습니다.' in reference_case_content:
            aiRelatedLaw = '관련 판례를 찾지 못하였습니다.'

        result = {
            "aiDescription": results[0]['description'],
            "aiExplanation": results[0]['explanation'],
            "aiResult": results[0]['Result'],
            "aiRelatedLaw": aiRelatedLaw,
            "aiUserFault": ai_result[5],
            "aiOtherFault": ai_result[4]
        }

        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print(result)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')

  
        return JSONResponse(content=result)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        traceback.print_exc()  # 상세한 오류 정보를 출력
        raise HTTPException(status_code=400, detail=f"Error processing video file: {str(e)}")
    finally:
        # 임시 파일 및 디렉토리 정리
        if 'cap' in locals():
            cap.release()
        import time
        time.sleep(1)  # 파일 사용이 완전히 끝났는지 확인하기 위한 짧은 대기
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
                print(f"Temporary video file removed: {temp_video_path}")
            except PermissionError:
                print(f"Warning: Unable to delete temporary file: {temp_video_path}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Temporary directory removed: {temp_dir}")








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