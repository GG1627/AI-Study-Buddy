# Import the OpenCV module
import cv2

# Capture the video
capture = cv2.VideoCapture("../data/videos/example_video.mp4")

# Initialize the frame number to 0
f = 0

# Store the frames of the video
while(capture.isOpened()):
    ret, frame= capture.read()
    if ret == False:
        break

    # Save the frame to a specified directory
    cv2.imwrite("../data/frames/frame_" + str(f) + ".jpg", frame)
    f += 1

    