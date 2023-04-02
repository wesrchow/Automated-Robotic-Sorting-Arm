import sys
import threading
import traceback
from jetson_utils import videoSource, videoOutput, cudaAllocMapped
import torch
import cv2
import time

class Stream(threading.Thread):
    """
    Thread for streaming video and applying DNN inference
    """
    def __init__(self, args):
        super().__init__()
        print("loading")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', '/home/nvidia/P2_L2B_G8/Machine Learning/best.pt')
        print("finish loading")
        self.args = args
        # default from /dev/video0
        self.input = videoSource(args.input, argv=sys.argv)
        # self.cap = cv2.VideoCapture(args.input)
        self.output = videoOutput(args.output, argv=sys.argv)
        self.frames = 0

    def process(self):
        # Read the next frame from the video file
        # ret, frame = self.cap.read()

        img = self.input.Capture()

        if img is None:  # timeout
            return

        # if not ret or frame is None:
        #     return

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Perform object detection on the current frame using the YOLOv5 model
        results = self.model(img)

        # Draw bounding boxes around the detected objects
        # results.render()

        # Display the results
        # cv2.imshow('Object Detection', cv2.cvtColor(results.render()[0]))


        # Capture one image from the stream, process it, and output it.
                
        # if self.args.detection:
        #     detections = self.net.Detect(img, overlay="box,labels,conf")

        #     print(f"detected {len(detections)} objects")

        #     for detection in detections:
        #         print(detection)

        print("render img")
        self.output.Render(img)

        if self.frames % 25 == 0 or self.frames < 15:
            print(f"captured {self.frames} frames from {self.args.input} => {self.args.output} ({img.width} x {img.height})")
            print(results.pandas.xyxy[0])
   
        self.frames += 1
        
    def run(self):
        """
        Run the stream processing thread's main loop.
        """
        while True:
            try:
                self.process()
            except:
                traceback.print_exc()
                
    @staticmethod
    def usage():
        """ 
        Return help text for when the app is started with -h or --help
        """
        return videoSource.Usage() +videoOutput.Usage() 
        