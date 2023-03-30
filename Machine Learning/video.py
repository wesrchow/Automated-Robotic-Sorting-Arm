import torch
from flask import Flask, render_template, Response
import cv2

# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/xxni/UBC/CPEN291/Project2/yolov5/runs/train/exp/weights/best.pt')

# Define the index of your webcam (usually 0 or 1)
webcam_index = 0

# Open the webcam using OpenCV
cap = cv2.VideoCapture(webcam_index)

# Define the output video codec and dimensions
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter('/Users/xxni/UBC/CPEN291/Project2/output.mp4', fourcc, fps, (width, height))

# Loop over each frame in the video file
while cap.isOpened():
    # Read the next frame from the video file
    ret, frame = cap.read()
    
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Perform object detection on the current frame using the YOLOv5 model
        results = model(frame)

        # Draw bounding boxes around the detected objects
        results.render()

        # Display the results
        cv2.imshow('Object Detection', cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR))

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release the video file and output video file
cap.release()
out.release()

# Close all windows
cv2.destroyAllWindows()
