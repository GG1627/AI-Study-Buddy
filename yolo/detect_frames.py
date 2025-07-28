from ultralytics import YOLO
from pathlib import Path
import os
import re
import json

# Declare the YOLO model
# model = YOLO("yolo11n.pt")

# load trained model
model = YOLO("../runs/detect/train/weights/best.pt")
# results = model("../data/frames/frame_0.jpg")

# declare frames folder path
frames_folder = Path("../data/frames")

# output JSON dictionary
detection_data = {}

CLASS_NAMES = {0: "cup", 1: "tray"}

# numberic sorting helper
def numeric_key(path):
    match = re.search(r"(\d+)", path.stem)
    return int(match.group(1)) if match else -1

# Sort frame files numerically
frame_files = sorted([f for f in frames_folder.iterdir() if f.is_file()], key=numeric_key)

# loop through each frame in the frames folder
for item in frame_files:
    if item.is_file():
        # Send each frame to the trained YOLO model
        results = model(item)

        frame_detections = []
        
        
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Get the coordinates in xyxy format
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()

                confidence = float(box.conf[0].item())
                class_id = int(box.cls[0].item())

                detection = {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "confidence": confidence,
                    "class_id": class_id,
                    "label": CLASS_NAMES.get(class_id, "unknown")
                }

                frame_detections.append(detection)

        detection_data[item.stem] = frame_detections


    else:
        print("No files found")

with open("frame_detections.json", "w") as f:
    json.dump(detection_data, f, indent=2)

print("\n✅ All detections saved to 'frame_detections.json'")



                