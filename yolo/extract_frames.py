# Import the OpenCV module
import cv2
import pathlib
import shutil
from pathlib import Path

def run(video_path=None):
    # Get absolute path from project root
    project_root = Path(__file__).parent.parent
    frames_dir = project_root / "data" / "temp_frames"

    print(f"📹 Processing video: {video_path}")
    print(f"🗂️ Clearing and creating frames directory: {frames_dir}")

    # Clear the frames folder to avoid contamination from previous videos
    if frames_dir.exists():
        shutil.rmtree(frames_dir)

    # Create fresh new frames directory
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Capture the video
    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise ValueError(f"❌ Could not open video file: {video_path}")

    # Initialize the frame number to 0
    f = 0

    # Store the frames of the video
    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret == False:
            break

        # Save the frame using the correct absolute path
        frame_path = frames_dir / f"frame_{f}.jpg"
        cv2.imwrite(str(frame_path), frame)
        f += 1

    capture.release()
    print(f"✅ Extracted {f} frames to {frames_dir}")
    
    if f == 0:
        raise ValueError(f"❌ No frames were extracted from video: {video_path}")
