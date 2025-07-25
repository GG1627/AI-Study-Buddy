from ultralytics import YOLO

# Declare the YOLO model
model = YOLO("yolo11n.pt")
results = model("../data/frames/frame_0.jpg")

# Show the results
for result in results:
    boxes = result.boxes

    for box in boxes:
        # Get the coordinates in xyxy formate
        x1, y1, x2, y2 = box.xyxy[0].int().tolist()

        confidence = box.conf[0].item()
        class_id = box.cls[0].item()

        print(f"Coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        print(f"Confidence: {confidence:.2f}, Class ID: {class_id}")