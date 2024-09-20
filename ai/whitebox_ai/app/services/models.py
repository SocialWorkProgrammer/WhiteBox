from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# lawyer Table 데이터
class Lawyer(Base):
    __tablename__ = "lawyer"
    id = Column(Integer, primary_key=True, index=True)
    lawyer_name = Column(String(255))
    lawyer_date = Column(Date)
    lawyer_image_url = Column(String(255))