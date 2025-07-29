from yolo import track_object, detect_frames as df_module, extract_frames as ef_module
import fastapi as _fastapi
from fastapi import File, UploadFile, FastAPI, HTTPException
from pathlib import Path
import shutil
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
import boto3
import uuid
import sys
import os
import cv2
from dotenv import load_dotenv
from backend.s3_utils import download_from_s3

# load environment variables
load_dotenv()

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# set up FastAPI app
app = _fastapi.FastAPI()


"""
Add CORS middleware so your Next.js frontend can talk to this API
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-study-buddy-front-end.onrender.com",
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

"""
Set up AWS S3 Client
"""
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# simple health check
@app.get("/")
def root():
    return {"status": "SurgiTrack backend is running ✅"}

# async await to run the track_object.run function in a separate thread because it takes a while to run
@app.get("/events")
async def get_tracking_events():
    logger.info("/events endpoint hit")
    return await asyncio.to_thread(track_object.run)

# async await to run the detect_frames.run function in a separate thread because it takes a while to run
@app.get("/detect")
async def detect_frames():
    logger.info("/detect endpoint hit")
    return await asyncio.to_thread(df_module.run)

# async await to run the extract_frames.run function in a separate thread because it takes a while to run
@app.get("/extract")
async def extract_frames():
    logger.info("/extract endpoint hit")
    return await asyncio.to_thread(ef_module.run)

@app.post("/process")
async def process_video(file_key: str):
    temp_video_path = None
    try:
        logger.info(f"🚀 Starting video processing for file_key: {file_key}")

        # Create the temp_videos directory if it doesn't exist
        temp_videos_dir = Path("data/temp_videos")
        temp_videos_dir.mkdir(parents=True, exist_ok=True)
        
        # Define temp file path
        temp_video_path = temp_videos_dir / file_key

        # Download the video from S3
        logger.info("📥 Downloading video from S3...")
        download_from_s3(file_key, str(temp_video_path))
        logger.info(f"✅ Successfully downloaded video to: {temp_video_path}")

        # Call the pipeline
        logger.info("🎬 Extracting frames...")
        ef_module.run(str(temp_video_path))
        logger.info("✅ Frame extraction completed")
        
        logger.info("🤖 Running object detection...")
        df_module.run()
        logger.info("✅ Object detection completed")
        
        logger.info("📊 Tracking objects...")
        results = track_object.run()
        logger.info(f"✅ Processing complete! Found {len(results)} events")

        return {"events": results, "file_key": file_key}
    
    except Exception as e:
        logger.error(f"❌ Error processing video {file_key}: {e}")
        raise _fastapi.HTTPException(status_code=500, detail=str(e))
    
    # Delete the temp video file
    finally:
        if temp_video_path and temp_video_path.exists():
            logger.info(f"🗑️ Cleaning up temp file: {temp_video_path}")
            temp_video_path.unlink()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Starting upload for file: {file.filename}")
        
        # Check environment variables
        bucket_name = os.getenv("S3_BUCKET_NAME")
        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION")
        
        if not all([bucket_name, aws_key, aws_secret, aws_region]):
            logger.error("Missing AWS environment variables")
            raise _fastapi.HTTPException(status_code=500, detail="AWS configuration missing")
        
        logger.info(f"Using bucket: {bucket_name}")


        # Check if the file is an mp4 
        if not file.filename.lower().endswith("mp4"):
            raise _fastapi.HTTPException(status_code=400, detail="❌ Only .mp4 files are allowed.")
        
        # Check if the file size is less than 10MB
        if file.size > 10 * 1024 * 1024:
            raise _fastapi.HTTPException(status_code=400, detail="❌ File size exceeds 10MB limit.")
        
        # Read the file content
        file_content = await file.read()

        # Check if the file frame rate is less than 60 FPS
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            cap = cv2.VideoCapture(temp_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()

            if fps > 60:
                raise _fastapi.HTTPException(status_code=400, detail="❌ File frame rate exceeds 60 FPS.")
            
        finally:
            os.unlink(temp_file_path)

        # Upload the file to AWS S3 bucket
        file_key = f"{uuid.uuid4()}_{file.filename}"


        s3_client.put_object(
            Bucket=os.getenv("S3_BUCKET_NAME"),
            Key=file_key,
            Body=file_content,
            ContentType=file.content_type
        )

        return {"filename": file.filename, "file_key": file_key, "status": "✅ Upload successful"}
    
    except Exception as e:
        logger.error(f"❌ Error uploading file: {e}")
        raise _fastapi.HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)