import Arm
if __name__ == "__main__":

    base = Base(0)
    shoulder = Shoulder(0)
    elbow = Elbow(0)
    wrist = Wrist(0)

    while True:
        base.base_servo.angle = 50
        shoulder.shoulder_servo.angle = 50
        elbow.elbow_servo.angle = 50
        wrist.wrist_servo.angle = 50
