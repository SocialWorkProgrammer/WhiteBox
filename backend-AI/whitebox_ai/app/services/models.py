from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy.orm import declarative_base
from ..core.database import Base
from pydantic import BaseModel, Field

# lawyer Table 데이터
class Lawyer(Base):
    __tablename__ = "lawyer"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_name = Column(String(255))
    lawyer_date = Column(Date)
    lawyer_image_url = Column(String(255))

class Result(BaseModel):
    # 사고 상황, 과실 해설, 최종 결론
    description: str = Field()
    explanation: str = Field()
    Result: str = Field()

class QueryRequest(BaseModel):
    query_text: str
    accident_location: str
    a_direction: str
    b_direction: str
    a_percentage: str
    b_percentage: str
    accident_location_description: str