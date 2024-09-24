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

load_dotenv()

router = APIRouter()

metrics = ["cosine", "euclidean","euclidean_12"]

class Settings(BaseSettings):
    authjwt_secret_key : str = os.getenv("SECRET_KEY")

@AuthJWT.load_config
def get_config():
    return Settings()

@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decoded_token):
    return False  


@router.post("/api/v1/lawyer")
async def compare_image(
    name : str, date : str, file: UploadFile = File(...), db: Session = Depends(get_db), Authorize: AuthJWT = Depends() 
):
    
    try:
        Authorize.jwt_required()  
    except KeyError as e:
        if 'type' in str(e):
            pass  
        else:
            raise e  

    user_email = Authorize.get_raw_jwt().get('username') 
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_name == name, Lawyer.lawyer_date == date).first()

    if not lawyer:
        return HTTPException(status_code=404, detail="변호사 인증 실패!")
    
    answer = url_to_img(lawyer.lawyer_image_url)
    input = byte_to_img(await file.read())
    result = DeepFace.verify(img1_path = answer, img2_path = input) 
    distance = result['distance']

    if distance <= 0.3: 
        db.execute(text("UPDATE user SET user_type = 'LAWYER' WHERE user_email = :user_email"), {"user_email": user_email})
        db.commit()

        return JSONResponse(content={"message": "변호사 인증 성공!", "user_type": "LAWYER"})
    else:
        return JSONResponse(content={"message": "변호사 인증 실패", "user_type":"MEMBER"}) 