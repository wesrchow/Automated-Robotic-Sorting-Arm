# Arm control algorithm to pick up and drop components stored in "detetion.json"
import Arm
import time
import json
import RPi.GPIO as GPIO

class arm_controller:
    magnet = 18 # pin 12
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(magnet, GPIO.OUT, initial=GPIO.HIGH)

    def grab(self):
        GPIO.output(self.magnet, GPIO.HIGH)
        
    def  release(self):
        GPIO.output(self.magnet, GPIO.LOW)


    def get_components_from_json(file_path):
        # Load the data from the JSON file
        with open(file_path, 'r') as f:
            detections = json.load(f)

        # Create dictionaries to store the components for each category
        resistor_components = []
        capacitor_l_components = []
        led_red_components = []
        capacitor_components = []

        # Loop through each detection and extract the components by category
        for detection in detections:
            if detection['name'] == 'resistor':
                resistor_components.append(detection)
            elif detection['name'] == 'capacitor_L':
                capacitor_l_components.append(detection)
            elif detection['name'] == 'LED_red':
                led_red_components.append(detection)
            elif detection['name'] == 'capacitor':
                capacitor_components.append(detection)

        # Return a dictionary with the components for each category
        return {
            'resistor': resistor_components,
            'capacitor_L': capacitor_l_components,
            'LED_red': led_red_components,
            'capacitor': capacitor_components
        }


    def sort_resistor(x_sent, y_sent):
        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50
            wrist.interAngle = wrist.finAngle - 50

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 5
            else:
                shoulder.finAngle = shoulder.finAngle - 6

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

            time.sleep(1.5)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 4:
            elbow.set_angle_conv(90)
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 5:
            base.base_servo.angle = 45
            time.sleep(0.5)
            base.base_servo.angle = 0
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

    def sort_capacitor(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50
            wrist.interAngle = wrist.finAngle - 50

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 5
            else:
                shoulder.finAngle = shoulder.finAngle - 6

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

            time.sleep(1.5)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 4:
            elbow.set_angle_conv(90)
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 5:
            base.base_servo.angle = 90
            time.sleep(0.5)
            base.base_servo.angle = 45
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

    def sort_capacitor_l(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50
            wrist.interAngle = wrist.finAngle - 50

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 5
            else:
                shoulder.finAngle = shoulder.finAngle - 6

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

            time.sleep(1.5)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 4:
            elbow.set_angle_conv(90)
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 5:
            base.base_servo.angle = 90
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

    def sort_inductor(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50
            wrist.interAngle = wrist.finAngle - 50

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 5
            else:
                shoulder.finAngle = shoulder.finAngle - 6

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

            time.sleep(1.5)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 4:
            elbow.set_angle_conv(90)
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 5:
            base.base_servo.angle = 90
            time.sleep(0.5)
            base.base_servo.angle = 135
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

    def sort_led(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


        if base.state == 1:
            base.update_dist(x_sent, y_sent)
            Arm.update_distances(base, shoulder, elbow, wrist)
            base.point_arm(x_sent, y_sent)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50
            wrist.interAngle = wrist.finAngle - 50

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 5
            else:
                shoulder.finAngle = shoulder.finAngle - 6

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

            time.sleep(1.5)

        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 4:
            elbow.set_angle_conv(90)
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(2)

        if base.state == 5:
            base.base_servo.angle = 135
            time.sleep(0.5)
            base.base_servo.angle = 180
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)
            
            
    def sort_all_resistors(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort resistor
        resistor_components = components['resistor']
        for resistor in resistor_components:
            if resistor['confidence'] > 0.4:
                x_input = (resistor['xmin'] + resistor['xmax'])/2
                y_input = (resistor['ymin'] + resistor['ymax'])/2 
                y_input = 480 - y_input
                self.sort_resistor(x_input, y_input)

    def sort_all_capacitors(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort capacitor
        capacitor_components = components['capacitor']
        for capacitor in capacitor_components:
            if capacitor['confidence'] > 0.4:
                x_input = (capacitor['xmin'] + capacitor['xmax'])/2
                y_input = (capacitor['ymin'] + capacitor['ymax'])/2
                y_input = 480 - y_input
                self.sort_capacitor(x_input, y_input)


    def sort_all_capacitors_L(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort capacitor_L
        capacitor_l_components = components['capacitor_L']
        for capacitor_l in capacitor_l_components:
            if capacitor_l['confidence'] > 0.4:
                x_input = (capacitor_l['xmin'] + capacitor_l['xmax'])/2
                y_input = (capacitor_l['ymin'] + capacitor_l['ymax'])/2
                y_input = 480 - y_input
                self.sort_capacitor_l(x_input, y_input)
                
        print("here12345")

    def sort_all_led_red(self):
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort led_red
        led_red_components = components['LED_red']
        print(led_red_components)
        for led_red in led_red_components:
            if led_red['confidence'] > 0.4:
                x_input = (led_red['xmin'] + led_red['xmax'])/2
                y_input = (led_red['ymin'] + led_red['ymax'])/2
                y_input = 480 - y_input
                self.sort_led(x_input, y_input)
        
    def sort_all_components(self):
        self.sort_all_led_red(self)
        self.sort_all_resistors(self)
        self.sort_all_capacitors(self)
        # self.sort_all_capacitors_L(self)
        