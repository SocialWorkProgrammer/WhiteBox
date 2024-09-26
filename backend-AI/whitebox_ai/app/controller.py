from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.models import Lawyer
from app.services.service import url_to_img, byte_to_img
from app.core.database import get_db
from deepface import DeepFace
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings
from sqlalchemy import text
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
