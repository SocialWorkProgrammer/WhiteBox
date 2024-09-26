from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL ="mysql+pymysql://root:ssafy@localhost/whitebox"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)
Base = declarative_base()
# DB 세션 생성

def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()
