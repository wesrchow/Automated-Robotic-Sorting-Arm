import math
import board


class Arm:
    def __init__(self, angle):
        self.angle = angle
        state = 0


class Base(Arm):
    def __init__(self, angle):
        super().__init__(angle)
        self.finAngle = angle
        pwm_base = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        base_servo = servo.Servo(pwm_base)


class Shoulder(Arm):
    def __init__(self, angle):
        super().__init__(angle)
        self.finAngle = angle
        # pwm_shoulder = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        # shoulder_servo = servo.Servo(pwm_shoulder)


class Elbow(Arm):
    def __init__(self, angle):
        super().__init__(angle)
        self.finAngle = angle
        # pwm_arm_elbow = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        # elbow_servo = servo.Servo(pwm_arm_elbow)


class Wrist(Arm):
    def __init__(self, angle):
        super().__init__(angle)
        self.finAngle = angle
        # pwm_arm_wrist = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        # wrist_servo = servo.Servo(pwm_arm_wrist)

    def updateAng(self, shoulderAng):

