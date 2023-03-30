import Arm
import time

if __name__ == "__main__":

    prob_min = 0.50
    base = Arm.Base(0)
    shoulder = Arm.Shoulder(115)
    elbow = Arm.Elbow(70)
    wrist = Arm.Wrist(45)
    x_sent = 1
    y_sent = 1
    x_prev = -1
    y_prev = -1
    prob_sent = 0.9
    while True:
        if x_sent != x_prev and y_sent != y_prev and prob_sent > prob_min:
            Arm.update_state(base, shoulder, elbow, wrist)
            x_prev = x_sent
            y_prev = y_sent

        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(1)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)
            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                  wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                     shoulder.fore_arm_length) - shoulder.base_angle_offset
            # shoulder.interAngle, wrist.interAngle = Arm.cosine_law_side(elbow.finAngle,
            #                                                             wrist.wrist_length, shoulder.humerus_length)
            #
            shoulder.interAngle = shoulder.finAngle + 25
            wrist.interAngle = shoulder.finAngle - 25
            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)
            #### write the magnet to high ####
            time.sleep(1)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 5)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(1)

        if base.state == 4:
            elbow.set_angle_conv(70)
            wrist.set_angle_conv(45)
            shoulder.set_angle_conv(115)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(1)

        if base.state == 5:
            base.base_servo = 0
            time.sleep(3)
            #### write the magnet to low ####
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

        #x_sent = val from website
        #y_sent = val from website
        #prob_set = val from website

