from fastapi import FastAPI, UploadFile, File, HTTPException
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    logger.info(f"Received request to analyze video")
    logger.debug(f"Request headers: {dict(file.headers)}")
    
    try:
        logger.info(f"Received file: {file.filename}")
        file_content = await file.read()
        logger.info(f"File size: {len(file_content)} bytes")
        
        file.file.seek(0)
        
        result = {
            "aiRelatedInformation": "Sample AI Information",
            "aiRelatedLaw": "Sample AI Law",
            "aiUserFault": 80,
            "aiOtherFault": 20
        }
        logger.info(f"Returning result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Error processing file")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)