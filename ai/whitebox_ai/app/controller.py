from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.models import Lawyer
from app.services.service import image_to_bytes
from app.core.database import get_db

router = APIRouter()


@router.post("/ap1/v1/lawyer")
async def compare_image(
    name : str, date :  str,  file: UploadFile = File(...), db: Session = Depends(get_db)
):
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_name == name, Lawyer.lawyer_date == date).first()

    if not lawyer:
        return HTTPException(status_code=404, detail="변호사 인증 실패!")
    
    answer = image_to_bytes(lawyer.image)
    input = image_to_bytes(await file.read())

    return {"similarity : similarity"}
    
    # DB 이미지 PIL 이미지로 변환
