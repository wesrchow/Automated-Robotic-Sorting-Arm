import Arm
import time

if __name__ == "__main__":

    prob_min = 0.50
    base = Arm.Base(0)
    shoulder = Arm.Shoulder(50)
    time.sleep(10)
    elbow = Arm.Elbow(120)
    wrist = Arm.Wrist(95)
    prob_sent = 0



