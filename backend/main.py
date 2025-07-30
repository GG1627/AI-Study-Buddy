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
import os
from dotenv import load_dotenv
from backend.s3_utils import download_from_s3
from upstash_redis import Redis as UpstashRedis
import json

# load environment variables
load_dotenv()

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# set up FastAPI app
app = _fastapi.FastAPI()

# configure redis connection using Upstash REST API
upstash_url = os.getenv("UPSTASH_REDIS_REST_URL")
upstash_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

if not upstash_url or not upstash_token:
    raise ValueError("UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables are not set")

# Create Upstash REST client
upstash_redis = UpstashRedis(url=upstash_url, token=upstash_token)

# Simple job queue for worker
def enqueue_job(func_name, *args, **kwargs):
    job_id = kwargs.get('job_id', str(uuid.uuid4()))
    job_data = {
        "func_name": func_name,
        "args": args,
        "kwargs": kwargs,
        "job_id": job_id,
        "status": "queued"
    }
    upstash_redis.lpush("job_queue", json.dumps(job_data))
    return job_id


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
    """Queue tracking job instead of processing directly"""
    job_id = enqueue_job("track_object.run")
    return {"job_id": job_id, "status": "Job queued for tracking events"}

# async await to run the detect_frames.run function in a separate thread because it takes a while to run
@app.get("/detect")
async def detect_frames():
    """Queue detection job instead of processing directly"""
    job_id = enqueue_job("detect_frames.run")
    return {"job_id": job_id, "status": "Job queued for detection"}

# async await to run the extract_frames.run function in a separate thread because it takes a while to run
@app.get("/extract")
async def extract_frames():
    """Queue extraction job instead of processing directly"""
    job_id = enqueue_job("extract_frames.run")
    return {"job_id": job_id, "status": "Job queued for extraction"}

@app.post("/process")
async def process_video(file_key: str):
    # generate a unique job ID
    job_id = str(uuid.uuid4())
    
    # Enqueue the job instead of processing immediately
    job = enqueue_job("yolo.jobs.process_pipeline", file_key, job_id, job_id=job_id)
    
    logger.info(f"🚀 Enqueued video processing job {job_id} for file_key: {file_key}")
    
    return {"job_id": job_id, "status": "Job queued successfully"}

@app.get("/job/{job_id}")
async def get_job_status(job_id: str):
    # This part of the code was not provided in the edit_specification,
    # so it will remain as is, assuming the user will provide the implementation
    # for fetching job status from the Upstash Redis queue.
    # For now, we'll return a placeholder response.
    return {"job_id": job_id, "status": "Not implemented yet"}

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