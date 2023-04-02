import torch
# from flask import Flask, render_template, Response
import cv2
import time
# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', '/home/nvidia/P2_L2B_G8/Machine Learning/best.pt')

# Open the webcam using OpenCV
cap = cv2.VideoCapture("/dev/video0")
past = time.time()

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

    if (time.time() - past > 5):
        print(results.pandas().xyxy[0])
        past = time.time()

# Release the video file and output video file
cap.release()
# out.release()

# Close all windows
cv2.destroyAllWindows()