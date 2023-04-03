import torch
# from flask import Flask, render_template, Response
import cv2
import time
import json

# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')

# Open the webcam using OpenCV
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")
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

    with open("capture.json",'r') as f:
        capture = json.load(f)
        if (capture is True):
            with open("sample.json", "w") as outfile:
                outfile.dumps(results.pandas().xyxy[0].sort_values("class").to_json(orient="records"))

    if (capture is True):
        with open("capture.json",'w') as f:
            capture = False
            json.dump(capture, f)


# Release the video file and output video file
cap.release()
# out.release()

# Close all windows
cv2.destroyAllWindows()