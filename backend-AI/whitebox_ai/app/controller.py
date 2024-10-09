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

dict_label = {
  "0": [
    "차도와 차도가 아닌 장소",
    "차도가 아닌 장소에서 차도로 진입",
    "차도에서 직진",
    "차도가 아닌 장소에서 우회전 진입",
    20,
    80
  ],
  "1": [
    "차도와 차도가 아닌 장소",
    "차도에서 차도가 아닌 장소로 진입",
    "차도에서 직진",
    "차도가 아닌 장소로 중앙선 침범 진입",
    0,
    100
  ],
  "2": [
    "차도와 차도가 아닌 장소",
    "차도가 아닌 장소에서 차도로 진입",
    "차도에서 직진",
    "차도가 아닌 장소에서 중앙선 침범 진입",
    0,
    100
  ],
  "3": [
    "직선 도로",
    "추돌 사고",
    "후행 추돌",
    "선행 직진",
    100,
    0
  ],
  "4": [
    "차도와 차도가 아닌 장소",
    "차도가 아닌 장소에서 차도로 진입",
    "차도에서 직진",
    "차도가 아닌 장소에서 차도로 진입",
    10,
    90
  ],
  "5": [
    "주차장(또는 차도가 아닌 장소)",
    "주차구역과 통로",
    "통로 직진",
    "주차구역에서 직진 출자",
    30,
    70
  ],
  "6": [
    "직선 도로",
    "차로변경(진로변경)",
    "동시 차로변경(진로변경)",
    "동시 차로변경(진로변경)",
    50,
    50
  ],
  "7": [
    "직선 도로",
    "차로변경(진로변경)",
    "후행 직진",
    "선행 진로변경",
    30,
    70
  ],
  "8": [
    "직선 도로",
    "이면도로 교행 사고",
    "[마주보며] 직진",
    "[마주보며] 직진",
    50,
    50
  ],
  "9": [
    "직선 도로",
    "추월 사고",
    "선행 직진",
    "급접거리 추월(점선 중앙선)",
    0,
    100
  ],
  "10": [
    "직선 도로",
    "차로 감소 도로 (합류)",
    "본선에서 직진",
    "차로 감소 도로에서 본선으로 합류",
    40,
    60
  ],
  "11": [
    "직선 도로",
    "역주행 사고(중앙선 침범)",
    "직진",
    "중앙선 침범 직진",
    0,
    100
  ],
  "12": [
    "직선 도로",
    "추돌 사고",
    "주(정)차",
    "후행 추돌",
    0,
    100
  ],
  "13": [
    "직선 도로",
    "추월 사고",
    "실선 추월",
    "선행 직진",
    100,
    0
  ],
  "14": [
    "직선 도로",
    "차로변경(진로변경)",
    "정체차로에서 대기 중 진로변경(측면 충돌)",
    "직진(측면 충돌)",
    100,
    0
  ],
  "15": [
    "직선 도로",
    "정차 후 출발 사고",
    "정차 후 출발",
    "추월",
    80,
    20
  ],
  "16": [
    "직선 도로",
    "추돌 사고",
    "선행자동차(1차사고차량)를 추돌",
    "선행자동차(1차사고차량)",
    80,
    20
  ],
  "17": [
    "직선 도로",
    "안전지대 통과 사고",
    "후행 직진(안전지대 벗어나기 전)",
    "선행 진로변경",
    100,
    0
  ],
  "18": [
    "직선 도로",
    "추월 사고",
    "중앙선 침범 추월(후방)",
    "중앙선 침범 추월(전방)",
    60,
    40
  ],
  "19": [
    "직선 도로",
    "추월 사고",
    "선행 직진",
    "추월(실선 중앙선)",
    0,
    100
  ],
  "20": [
    "직선 도로",
    "열린 문 접촉사고",
    "후행 직진",
    "선행 자동차(정차중 문열림)",
    20,
    80
  ],
  "21": [
    "사거리 교차로(신호등 없음)",
    "교차로 내 진로변경",
    "직진(교차로 내 진로변경)",
    "우회전",
    60,
    40
  ],
  "22": [
    "고속도로(자동차 전용도로)포함",
    "주행차로와 주행차로",
    "후행 직진",
    "주행차로에서 주행차로로 변경",
    30,
    70
  ],
  "23": [
    "고속도로(자동차 전용도로)포함",
    "추돌",
    "선행 차량 추돌",
    "선행 직진",
    100,
    0
  ],
  "24": [
    "사거리 교차로(신호등 있음)",
    "노면 표시 위반사고",
    "직진(직진.좌회전 노면표시차로)",
    "좌회전(직진 노면표시차로)",
    0,
    100
  ],
  "25": [
    "T자형 교차로",
    "동일폭 도로",
    "직진",
    "우회전",
    30,
    70
  ],
  "26": [
    "직선 도로",
    "긴급자동차 사고",
    "후행 직진",
    "선행 진로변경(긴급자동차)",
    90,
    10
  ],
  "27": [
    "직선 도로",
    "마주보는 이륜차와 자동차간의 사고",
    "직진",
    "중앙선을 침범하여 반대차로 진행",
    0,
    100
  ],
  "28": [
    "회전교차로",
    "회전차로 2차로형",
    "회전(회전 2차로)",
    "진로변경(회전 1차로 → 회전 2차로)",
    40,
    60
  ],
  "29": [
    "주차장(또는 차도가 아닌 장소)",
    "주차구역과 통로",
    "통로 직진",
    "주차구역에서 후진 출자",
    25,
    75
  ],
  "30": [
    "직선 도로",
    "안전지대 통과 사고",
    "후행 직진(안전지대 벗어난 후)",
    "선행 진로변경",
    70,
    30
  ],
  "31": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[녹색신호] 직진",
    "[적색신호] 직진",
    0,
    100
  ],
  "32": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[적색신호] 직진",
    "[적색신호] 직진",
    50,
    50
  ],
  "33": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "오른쪽에서 직진",
    "왼쪽에서 직진",
    40,
    60
  ],
  "34": [
    "고속도로(자동차 전용도로)포함",
    "합류",
    "본선에서 직진",
    "본선으로 합류",
    30,
    70
  ],
  "35": [
    "고속도로(자동차 전용도로)포함",
    "주행차로와 추월차로",
    "추월차로에서 직진",
    "주행차로에서 추월차로로 진로변경",
    20,
    80
  ],
  "36": [
    "고속도로(자동차 전용도로)포함",
    "주(정)차",
    "차로에서 주(정)차한 차량을 추돌",
    "차로에서 주(정)차",
    60,
    40
  ],
  "37": [
    "고속도로(자동차 전용도로)포함",
    "주행차로와 추월차로",
    "후행 직진",
    "추월차로에서 주행차로로 진로변경",
    30,
    70
  ],
  "38": [
    "고속도로(자동차 전용도로)포함",
    "낙하물",
    "낙화물에 의해 충격,회피중",
    "적재물 등의 낙하",
    0,
    100
  ],
  "39": [
    "고속도로(자동차 전용도로)포함",
    "주(정)차",
    "갓길에서 주(정)차한 차량을 추돌",
    "갓길에서 주(정)차",
    100,
    0
  ],
  "40": [
    "고속도로(자동차 전용도로)포함",
    "합류",
    "본선에서 직진",
    "차로 감소 도로에서 본선으로 합류",
    40,
    60
  ],
  "41": [
    "직선 도로",
    "추돌 사고",
    "후행 추돌",
    "선행 직진",
    100,
    0
  ],
  "42": [
    "고속도로(자동차 전용도로)포함",
    "갓길 진로변경",
    "갓길로 진로변경",
    "갓길 직진",
    60,
    40
  ],
  "43": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "[마주보며] 직진",
    "[마주보며] 좌회전",
    30,
    70
  ],
  "44": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "오른쪽 도로에서 직진",
    "왼쪽 도로에서 좌회전",
    30,
    70
  ],
  "45": [
    "사거리 교차로(신호등 없음)",
    "2개 차로 동시 우회전",
    "우회전(오른쪽 차로)",
    "우회전(왼쪽 차로)",
    30,
    70
  ],
  "46": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 직진",
    "소로에서 좌회전",
    20,
    80
  ],
  "47": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "왼쪽 도로에서 직진",
    "오른쪽 도로에서 좌회전",
    40,
    60
  ],
  "48": [
    "사거리 교차로(신호등 없음)",
    "2개 차량이 나란히 통행 가능한 차로폭",
    "후행 직진(차로 우측)",
    "선행 우회전(차로 좌측)",
    20,
    80
  ],
  "49": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "오른쪽에서 직진(후진입)",
    "왼쪽에서 직진(선진입)",
    70,
    30
  ],
  "50": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "우회전",
    "직진",
    60,
    40
  ],
  "51": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 직진",
    "소로에서 직진",
    30,
    70
  ],
  "52": [
    "사거리 교차로(신호등 없음)",
    "2개 차량이 나란히 통행 가능한 차로폭",
    "후행 직진(차로 좌측)",
    "선행 좌회전(차로 우측)",
    20,
    80
  ],
  "53": [
    "사거리 교차로(신호등 없음)",
    "정차 후 출발 사고",
    "정차 후 출발",
    "추월",
    80,
    20
  ],
  "54": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "오른쪽에서 직진(선진입)",
    "왼쪽에서 직진(후진입)",
    30,
    70
  ],
  "55": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 직진(후진입)",
    "소로에서 직진(선진입)",
    60,
    40
  ],
  "56": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 우회전(선진입)",
    "대로에서 직진(후진입)",
    50,
    50
  ],
  "57": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 좌회전",
    "대로에서 좌회전",
    70,
    30
  ],
  "58": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 우회전",
    "대로에서 직진",
    70,
    30
  ],
  "59": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "우회전(선진입)",
    "직진(후진입)",
    40,
    60
  ],
  "60": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 우회전",
    "소로에서 직진",
    30,
    70
  ],
  "61": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 직진(좌측도로)",
    "대로에서 좌회전(우측도로)",
    50,
    50
  ],
  "62": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 우회전(후진입)",
    "대로에서 직진(선진입)",
    80,
    20
  ],
  "63": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "우회전(후진입)",
    "직진(선진입)",
    70,
    30
  ],
  "64": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 직진(선진입)",
    "소로에서 직진(후진입)",
    20,
    80
  ],
  "65": [
    "사거리 교차로(신호등 없음)",
    "동일폭 도로",
    "오른쪽 도로에서 좌회전",
    "왼쪽 도로에서 좌회전",
    40,
    60
  ],
  "66": [
    "사거리 교차로(신호등 없음)",
    "좌/우회전 각도가 90도 미만",
    "후행 직진",
    "선행 좌회전",
    40,
    60
  ],
  "67": [
    "T자형 교차로",
    "동일폭 도로",
    "오른쪽 도로에서 좌회전",
    "왼쪽 도로에서 좌회전",
    40,
    60
  ],
  "68": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[녹색좌회전신호] 좌회전, [적색신호] 충돌",
    "[녹색신호] 직진",
    30,
    70
  ],
  "69": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "대로에서 우회전(후진입)",
    "소로에서 직진(선진입)",
    60,
    40
  ],
  "70": [
    "사거리 교차로(신호등 없음)",
    "대로와 소로",
    "소로에서 직진(우측도로)",
    "대로에서 좌회전(좌측도로)",
    45,
    55
  ],
  "71": [
    "회전교차로",
    "회전차로 1차로형",
    "회전교차로 진입",
    "교차로 내 회전",
    80,
    20
  ],
  "72": [
    "회전교차로",
    "회전차로 2차로형",
    "진로변경(회전 1차로 → 회전 2차로)",
    "회전교차로 진입",
    30,
    70
  ],
  "73": [
    "회전교차로",
    "회전차로 2차로형",
    "회전(회전 1차로)",
    "회전교차로 대진입",
    10,
    90
  ],
  "74": [
    "회전교차로",
    "회전차로 2차로형",
    "회전교차로 진입(1차로 → 회전 2차로)",
    "회전교차로 진입(2차로 → 회전 2차로)",
    60,
    40
  ],
  "75": [
    "T자형 교차로",
    "동일폭 도로",
    "오른쪽 도로에서 직진",
    "왼쪽 도로에서 좌회전",
    20,
    80
  ],
  "76": [
    "T자형 교차로",
    "대로와 소로",
    "소로에서 직진(우측도로)",
    "대로에서 좌회전(좌측도로)",
    35,
    65
  ],
  "77": [
    "T자형 교차로",
    "대로와 소로",
    "대로에서 직진",
    "소로에서 우회전",
    20,
    80
  ],
  "78": [
    "T자형 교차로",
    "대로와 소로",
    "대로에서 직진",
    "소로에서 좌회전",
    10,
    90
  ],
  "79": [
    "T자형 교차로",
    "동일폭 도로",
    "왼쪽 도로에서 직진",
    "오른쪽 도로에서 좌회전",
    30,
    70
  ],
  "80": [
    "T자형 교차로",
    "대로와 소로",
    "소로에서 직진",
    "대로에서 우회전",
    60,
    40
  ],
  "81": [
    "T자형 교차로",
    "대로와 소로",
    "대로에서 좌회전",
    "소로에서 좌회전",
    30,
    70
  ],
  "82": [
    "T자형 교차로",
    "대로와 소로",
    "소로에서 직진(좌측도로)",
    "대로에서 좌회전(우측도로)",
    40,
    60
  ],
  "83": [
    "T자형 교차로",
    "일시정지 표지가 한쪽방향에만 있음",
    "일시정지 위반 좌회전",
    "표지가 없는 도로에서 좌회전",
    80,
    20
  ],
  "84": [
    "T자형 교차로",
    "대로와 소로",
    "소로에서 좌회전",
    "대로에서 좌회전",
    70,
    30
  ],
  "85": [
    "사거리 교차로(신호등 있음)",
    "정차 후 출발 사고",
    "정차 후 출발",
    "추월",
    80,
    20
  ],
  "86": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 직진",
    "[녹색신호] 직진",
    80,
    20
  ],
  "87": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "[마주보며] 직진",
    "상시유턴구역에서 유턴",
    20,
    80
  ],
  "88": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[황색신호] 좌회전, [적색신호] 충돌",
    "[녹색신호] 직진",
    80,
    20
  ],
  "89": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [황색신호] 좌회전, [적색신호] 충돌",
    "(마주보며) [녹색신호] 직진",
    80,
    20
  ],
  "90": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [녹색신호] 직진",
    "(마주보며) [녹색신호] 좌회전 (비보호좌회전 아님)",
    0,
    100
  ],
  "91": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "[녹색좌회전신호] 좌회전",
    "맞은편 우회전",
    20,
    80
  ],
  "92": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[녹색신호] 직진, [적색신호] 충돌",
    "[녹색신호] 직진",
    30,
    70
  ],
  "93": [
    "사거리 교차로(신호등 있음)",
    "교차로 내 진로변경",
    "[녹색신호] 직진(교차로내 진로 변경)",
    "우회전",
    30,
    70
  ],
  "94": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 좌회전",
    "[적색신호] 직진",
    20,
    80
  ],
  "95": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "우회전(좌측도로)",
    "상시유턴구역에서 유턴",
    30,
    70
  ],
  "96": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 좌회전",
    "[녹색신호] 직진",
    90,
    10
  ],
  "97": [
    "사거리 교차로(신호등 있음)",
    "노면 표시 위반사고",
    "추월 우회전(직진 노면표시차로)",
    "직진(직진.우회전 노면표시차로)",
    100,
    0
  ],
  "98": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[적색신호] 직진",
    "[녹색좌회전신호] 좌회전",
    100,
    0
  ],
  "99": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 우회전",
    "[녹색신호] 직진",
    80,
    20
  ],
  "100": [
    "사거리 교차로(신호등 있음)",
    "노면 표시 위반사고",
    "[녹색직진.좌회전 신호] 후행 직진(좌회전 노면표시차로)",
    "[녹색직진.좌회전 신호] 선행 좌회전(직진좌회전 노면표시차로)",
    100,
    0
  ],
  "101": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[황색신호] 직진",
    "[적색신호] 좌회전",
    30,
    70
  ],
  "102": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 직진",
    "[적색신호] 직진",
    10,
    90
  ],
  "103": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [적색신호] 직진",
    "(마주보며) [녹색좌회전신호] 좌회전",
    100,
    0
  ],
  "104": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "[마주보며] 직진",
    "신호에 따른 유턴",
    100,
    0
  ],
  "105": [
    "사거리 교차로(신호등 있음)",
    "추월 사고",
    "중앙선 침범 추월",
    "[녹색좌회전신호] 좌회전",
    100,
    0
  ],
  "106": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[황색신호] 직진",
    "[적색신호] 직진",
    30,
    70
  ],
  "107": [
    "사거리 교차로(신호등 있음)",
    "노면 표시 위반사고",
    "[녹색 좌회전 신호] 직진 (좌회전 노면표시차로)",
    "[녹색 좌회전 신호] 좌회전 (직진·좌회전 노면표시차로)",
    100,
    0
  ],
  "108": [
    "사거리 교차로(신호등 있음)",
    "노면 표시 위반사고",
    "선행 우회전(직진·우회전 노면표시차로)",
    "후행 직진(우회전 노면표시차로)",
    0,
    100
  ],
  "109": [
    "사거리 교차로(신호등 있음)",
    "비보호 좌회전 표지 있음",
    "(마주보며) [녹색신호] 좌회전 (비보호 좌회전)",
    "(마주보며) [녹색신호] 직진",
    80,
    20
  ],
  "110": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[황색신호] 직진, [적색신호] 충돌",
    "[녹색신호] 직진",
    80,
    20
  ],
  "111": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [녹색 좌회전 신호] 좌회전, [적색신호 충돌]",
    "(마주보며) [녹색신호] 직진",
    30,
    70
  ],
  "112": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [적색신호] 직진",
    "(마주보며) [적색신호] 좌회전",
    50,
    50
  ],
  "113": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "우회전(좌측도로)",
    "신호에 따른 유턴",
    80,
    20
  ],
  "114": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "동시 유턴(선행)",
    "동시 유턴(후행)",
    20,
    80
  ],
  "115": [
    "사거리 교차로(신호등 있음)",
    "유턴구역",
    "유턴(선행)",
    "급 유턴(후행)",
    0,
    100
  ],
  "116": [
    "사거리 교차로(신호등 있음)",
    "긴급자동차 사고",
    "[녹색신호] 직진",
    "[적색신호] 직진 (긴급자동차)",
    60,
    40
  ],
  "117": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[적색신호] 직진",
    "[황색신호] 좌회전",
    60,
    40
  ],
  "118": [
    "사거리 교차로(신호등 있음)",
    "신호등이한쪽차량방향에만있음",
    "[무신호] 우회전",
    "[적색신호] 직진",
    10,
    90
  ],
  "119": [
    "사거리 교차로(신호등 있음)",
    "신호등이한쪽차량방향에만있음",
    "[무신호] 좌회전",
    "[황색신호] 직진",
    50,
    50
  ],
  "120": [
    "사거리 교차로(신호등 있음)",
    "신호등이 한쪽차량 방향에만 있음",
    "[무신호] 직진",
    "[황색신호] 직진",
    40,
    60
  ],
  "121": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [황색신호] 직진",
    "(마주보며) [녹색신호] 좌회전, [황색신호] 충돌",
    40,
    60
  ],
  "122": [
    "사거리 교차로(신호등 있음)",
    "상대 차량이 측면 방향에서 진입",
    "[적색신호] 직진",
    "[적색신호] 좌회전",
    50,
    50
  ],
  "123": [
    "사거리 교차로(신호등 있음)",
    "상대차량이 맞은편 방향에서 진입",
    "(마주보며) [황색신호] 직진",
    "(마주보며) [황색신호] 좌회전",
    50,
    50
  ]
}

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

# def run_mmaction2_inference():
#     cmd = [
#         "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/venv/Scripts/python.exe", "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/mmaction2/tools/test.py",
#         "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/slowfast_exp3.py",
#         "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/best_acc_top1_epoch_94.pth",
#         "--work-dir", "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace"
#     ]
#     subprocess.run(cmd, check=True)

def run_mmaction2_inference():
    cmd = [
        "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/venv/Scripts/python.exe",
        "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/mmaction2/tools/test.py",
        "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/slowfast_exp3.py",
        "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/best_acc_top1_epoch_94.pth",
        "--work-dir", "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace"
    ]
    
    # 환경 변수 설정
    env = os.environ.copy()
    env['PYTHONPATH'] = 'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai'
    
    # 작업 디렉토리 설정
    work_dir = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace"
    
    try:
        result = subprocess.run(cmd, check=True, env=env, cwd=work_dir, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Error output:", e.stderr)


def load_classification_results():
    with open("C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/result.pkl", 'rb') as f:
        results = pickle.load(f)
    return results


@router.post("/api/v1/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    detection_config_path = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/cascade_rcnn_cfg.py"
    detection_checkpoint_path = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/best_coco_bbox_mAP_epoch_10.pth"

    classification_config_path = "C:/Users/SSAFY/Downloads/slowfast_exp3.py"
    classification_checkpoint_path = "C:/Users/SSAFY/Downloads/best_acc_top1_epoch_94.pth"

    temp_dir = tempfile.mkdtemp()
    temp_video_path = None
    output_dir = os.path.expanduser("C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/images")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 업로드된 비디오를 임시 파일로 저장
        temp_video_fd, temp_video_path = tempfile.mkstemp(suffix='.mp4')
        with os.fdopen(temp_video_fd, 'wb') as temp_file:
            temp_file.write(await file.read())

        print(f"Temporary video saved at: {temp_video_path}")

        # CPU 설정
        device = torch.device("cpu")
        print(f"Using device: {device}")
        
        # 모델 초기화
        cfg = Config.fromfile(detection_config_path)
        model = init_detector(cfg, detection_checkpoint_path, device=device)
        class_names = model.dataset_meta['classes']
        print("Model initialized successfully")

        # 비디오 파일 열기
        cap = cv2.VideoCapture(temp_video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file")

        # 비디오 속성 가져오기
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video FPS: {fps}, Total frames: {total_frames}")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 리사이즈
            height, width = frame.shape[:2]
            new_width = 640
            new_height = int(height * (new_width / width))
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Bounding box 그리기
            frame_with_boxes = process_frame(model, resized_frame, class_names)

            # 결과 저장
            output_path = os.path.join(output_dir, f"img_{frame_count + 1:05d}.jpg")
            success = cv2.imwrite(output_path, frame_with_boxes)
            if not success:
                print(f"Failed to save image: {output_path}")
            else:
                print(f"Saved image: {output_path}")

            frame_count += 1

        cap.release()

        print(f"Total frames processed: {frame_count}")
        print(f"Output directory: {output_dir}")

        annotation_path = "C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/annotation.txt"
        with open(annotation_path, 'w') as f:
            f.write(f"images {frame_count}")


        run_mmaction2_inference()

        classification_results = load_classification_results()
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print(classification_results)
        print(classification_results[0]['pred_label'].item())
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')

        

        # result = {
        #     "aiDescription": "사고 발생 상황 분석",
        #     "aiExplanation": "과실 비율과 그 근거",
        #     "aiResult": "법적 기준 및 결론",
        #     "aiRelatedLaw": "관련 법(있을수도있고없을수도있음)",
        #     "aiUserFault": 80,
        #     "aiOtherFault": 20
        # }
        result = {
          "result" : dict_label[str(classification_results[0]['pred_label'].item())]
        }


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

    # try:
    #     async with httpx.AsyncClient() as client:
    #         spring_response = await client.post(
    #             "http://localhost/api/v1/upload-video",  
    #             json=response_data
    #         )
    #         spring_response.raise_for_status()
    # except httpx.HTTPStatusError as e:
    #     raise HTTPException(status_code=500, detail=f"Spring 서버로 전송 중 오류가 발생했습니다: {str(e)}")

    return JSONResponse(content=response_data)