import time
from Arm import Shoulder, Elbow, Wrist, Base
import json


class calibrate_run:
    def run_calibrate():
        # Initialize the servo motors
        shoulder = Shoulder(0)
        elbow = Elbow(90)
        wrist = Wrist(90)
        base = Base(90)

        # Set the servo angles to 90 degrees
        shoulder.set_angle_conv(90)
        elbow.set_angle_conv(90)
        wrist.set_angle_conv(90)
        base.raw_set(90)
        
        capture = "calibrate"
        with open('capture.json', 'w') as f:
            json.dump(capture, f)