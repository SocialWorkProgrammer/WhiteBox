from fastapi import FastAPI
from app.controller import router as lawyer_authorization_router
from app.core.database import Base, engine
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(lawyer_authorization_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host ="0.0.0.0", port=8000)