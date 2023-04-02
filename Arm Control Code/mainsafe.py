import Arm
import time

if __name__ == "__main__":

    prob_min = 0.50
    base = Arm.Base(0)
    shoulder = Arm.Shoulder(0)
    time.sleep(2)
    elbow = Arm.Elbow(90)
    wrist = Arm.Wrist(90)
    prob_sent = 0

    Arm.slow_move_synchro(wrist, shoulder, 120.0, 90.0, 10)
    print(shoulder.shoulder_servo_r.angle)
    print(shoulder.shoulder_servo_l.angle )



