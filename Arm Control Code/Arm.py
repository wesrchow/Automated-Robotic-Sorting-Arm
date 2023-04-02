import math
import board
import digitalio, busio
from adafruit_motor import servo
from adafruit_servokit import ServoKit


def conv_angle(anglerad):
    return (anglerad + math.pi / 2.0) * 180.0 / math.pi


def cosine_law_angle(side1, side2, side_across):
    angle = math.acos((side1 ** 2 + side2 ** 2 - side_across ** 2) / (2 * side1 * side2))
    return angle * 180 / math.pi


def cosine_law_side(angle_across, side1, side2):
    side3 = -(math.cos(angle_across * math.pi / 180.0) * 2 * side1 * side2 - side1 ** 2 - side2 ** 2)
    angle2 = cosine_law_angle(side1, side3, side2)
    angle1 = cosine_law_angle(side2, side3, side1)
    return angle1, angle2


def update_state(base, shoulder, elbow, wrist):
    if base.state < 5:
        base.state += 1
        shoulder.state += 1
        elbow.state += 1
        wrist.state += 1
    else:
        base.state = 0
        shoulder.state = 0
        elbow.state = 0
        wrist.state = 0


def update_distances(base, shoulder, elbow, wrist):
    shoulder.distance = base.distance
    shoulder.third_side = base.third_side
    shoulder.base_angle_offset = base.base_angle_offset

    elbow.distance = base.distance
    elbow.third_side = base.third_side
    elbow.base_angle_offset = base.base_angle_offset

    wrist.distance = base.distance
    wrist.third_side = base.third_side
    wrist.base_angle_offset = base.base_angle_offset


class Arm:
    kit = ServoKit(channels=16)
    pic_scale = 100
    picture_offset = 1
    base_height = 90
    wrist_length = 96
    fore_arm_length = 158
    humerus_length = 190
    base_servo = kit.servo[0]
    shoulder_servo_l = kit.servo[1]
    shoulder_servo_r = kit.servo[2]
    elbow_servo = kit.servo[3]
    wrist_servo = kit.servo[4]
    distance = None

    def __init__(self):
        self.state = 0
        self.wrist_height = self.base_height - self.wrist_length
        self.third_side = None
        self.base_angle_offset = None

    def update_dist(self, x, y):
        self.distance = math.sqrt((x * self.pic_scale) ** 2 + ((y + self.picture_offset) * self.pic_scale) ** 2)
        self.third_side = math.sqrt(int(self.distance) ** 2 + self.wrist_height ** 2)
        self.base_angle_offset = conv_angle(math.atan(self.wrist_height / self.distance))


class Base(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        self.base_servo.angle = angle
        self.base_servo.angle = angle

    def point_arm(self, x, y):
        center_x = x - 0.5
        center_y = y
        self.base_servo.angle = conv_angle(math.atan(center_x / (center_y+self.picture_offset/self.pic_scale)))


class Shoulder(Arm):
    inter_angle_offset = 30

    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        self.set_angle_conv(angle)
        self.length = self.humerus_length
        self.interAngle = None
        self.finAngle = None

    def set_angle_conv(self, angle):
        if angle > 90:
            angle = 90
        elif angle < 0:
            angle = 0
        self.shoulder_servo_r.angle = (90-angle) * 115.0 / 90.0
        self.shoulder_servo_l.angle = (115 - self.shoulder_servo_r.angle)*1.04348
        return

    def get_angle_conv(self, angle):
        if angle > 90:
            angle = 90
        elif angle < 0:
            angle = 0
        return (90-angle) * 115.0 / 90.0, 115 - (90-angle) * 115.0 / 90.0

    def conv_real(self, angle):
        if angle > 115
            angle = 115
        if angle < 0:
            angle = 0
        return (angle + 90)*90.0/115.0


class Elbow(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        self.set_angle_conv(angle)
        self.length = self.fore_arm_length
        self.finAngle = None

    def set_angle_conv(self, angle):
        if angle < 0:
            angle = 0
        elif angle > 130:
            angle = 130
        self.elbow_servo.angle = (180-angle) * 180.0 / 130.0
        return


class Wrist(Arm):
    def __init__(self, angle):
        super().__init__()
        self.finAngle = angle
        self.set_angle_conv(angle)
        self.length = self.wrist_length
        self.interAngle = None
        self.finAngle = None

    def set_angle_conv(self, angle):
        if angle < 90:
            angle = 90
        elif angle > 180:
            angle = 180
        self.wrist_servo.angle = (angle - 90) * 180.0 / 125.0
        return

    def conv_real(self, angle):
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0
        return (angle - 90)*125.0/180.0


def slow_move_synchro(wrist, shoulder, wrist_fin, shoulder_fin, divs):
    # conv_shoulder_fin_r, conv_shoulder_fin_l = shoulder.get_angle_conv(shoulder_fin)
    for i in range(0, divs):
        wrist.set_angle_conv((wrist.conv_real(wrist_fin) - wrist.wrist_servo.angle) / divs + wrist.wrist_servo.angle)
        shoulder.set_angle_conv(
            shoulder.shoulder_servo_r.angle + (shoulder.conv_real(shoulder_fin) - shoulder.shoulder_servo_r.angle) / divs)
        #if the potentionmeter is set off:
            #break
    return
