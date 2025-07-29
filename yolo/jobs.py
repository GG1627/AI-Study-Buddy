import logging
from pathlib import Path
from yolo import track_object, detect_frames as df_module, extract_frames as ef_module
from backend.s3_utils import download_from_s3

logger = logging.getLogger(__name__)


def process_pipeline(file_key: str, job_id: str):
    """
    Process video pipeline - this function will run in the background worker
    """
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
        raise e
    
    # Delete the temp video file
    finally:
        if temp_video_path and temp_video_path.exists():
            logger.info(f"🗑️ Cleaning up temp file: {temp_video_path}")
            temp_video_path.unlink()