import math
import microcontroller
import socketpool
import time, wifi, os, random
import board
import digitalio, pwmio, time, busio
from adafruit_motor import servo


def conv_angle(anglerad):
    return (anglerad + math.pi / 2.0) * 180.0 / math.pi


def cosine_law_angle(side1, side2, side_across):
    angle = math.acos((side1 ^ 2 + side2 ^ 2 - side_across ^ 2) / (2 * side1 * side2))
    return angle * 180 / math.pi


def cosine_law_side(angle_across, side1, side2):
    side3 = -(math.cos(angle_across * math.pi / 180.0) * 2 * side1 * side2 - side1 ^ 2 - side2 ^ 2)
    angle2 = cosine_law_angle(side1, side3, side2)
    angle1 = cosine_law_angle(side2, side3, side1)
    return side3, angle1, angle2


class Arm:
    pic_scale = 100
    base_height = 90
    wrist_length = 96
    fore_arm_length = 158
    humerus_length = 190

    def __init__(self):
        self.state = 0
        self.distance = None
        self.wrist_height = self.base_height - self.wrist_length
        self.third_side = None
        self.base_angle_offset = None

    def update_dist(self, x, y):
        self.distance = math.sqrt((x * self.pic_scale) ^ 2 + (y * self.pic_scale) ^ 2)
        self.third_side = math.sqrt(int(self.distance) ^ 2 + self.wrist_height ^ 2)
        self.base_angle_offset = conv_angle(math.atan(self.wrist_height / self.distance))


class Base(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        pwm_base = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        self.base_servo = servo.Servo(pwm_base)
        self.base_servo.angle = angle

    def point_arm(self, x, y):
        center_x = x - 0.5
        self.base_servo.angle = conv_angle(math.atan(center_x / y))
        self.state += 1


class Shoulder(Arm):
    inter_angle_offset = 30

    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        pwm_shoulder = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        self.shoulder_servo = servo.Servo(pwm_shoulder)
        self.shoulder_servo.angle = angle
        self.length = self.humerus_length
        self.interAngle = None
        self.finAngle = None


class Elbow(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        pwm_arm_elbow = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        self.elbow_servo = servo.Servo(pwm_arm_elbow)
        self.elbow_servo.angle = angle
        self.length = self.fore_arm_length
        self.finAngle = None


class Wrist(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        pwm_arm_wrist = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)
        self.wrist_servo = servo.Servo(pwm_arm_wrist)
        self.wrist_servo.angle = angle
        self.length = self.wrist_length
        self.interAngle = None
        self.finAngle = None


def slow_move_synchro(wrist, shoulder, wrist_fin, shoulder_fin, divs):
    for i in range(0, divs):
        wrist.wrist_servo.angle += (wrist_fin - wrist.wrist_servo.angle) / divs
        shoulder.shoulder_servo.angle += (shoulder_fin - shoulder.shoulder_servo.angle) / divs
        wrist.wrist_servo.angle = max(180, wrist.wrist_servo.angle)
        wrist.wrist_servo.angle = min(0, wrist.wrist_servo.angle)
        shoulder.shoulder_servo.angle = max(180, shoulder.shoulder_servo.angle)
        shoulder.shoulder_servo.angle = min(0, shoulder.shoulder_servo.angle)
    return
