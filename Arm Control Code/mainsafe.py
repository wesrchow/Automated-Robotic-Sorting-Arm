import Arm
import time

if __name__ == "__main__":

    prob_min = 0.50
    base = Arm.Base(0)
    shoulder = Arm.Shoulder(60)
    elbow = Arm.Elbow(120)
    wrist = Arm.Wrist(90)
    prob_sent = 0
    while True:
        time.sleep(3)
        Arm.slow_move_synchro(wrist, shoulder, 130, 20, 30)
        time.sleep(3)
        Arm.slow_move_synchro(wrist, shoulder, 90, 60, 30)


