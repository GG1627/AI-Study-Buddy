from ultralytics import YOLO

# Load base YOLOv11 model
model = YOLO("yolo11n.pt")

# Train it on your custom dataset
model.train(
    data="SurgiTrack-1/data.yaml",
    epochs=50,
    imgsz=640
)
