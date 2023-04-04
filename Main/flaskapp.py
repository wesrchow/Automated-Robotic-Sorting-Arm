from flask import Flask, send_file
from testing import SortingArm
from calibrate import calibrate_run
from sort import arm_controller

app = Flask(__name__)
arm = SortingArm()
calibrate_1 = calibrate_run
arm_controller_haha = arm_controller

@app.route('/calibrate')
def calibrate():
    arm.calibrate_arm()
    calibrate_1.run_calibrate()
    
    response = send_file("detection.jpg", mimetype='image/jpg')
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/sort-all')
def sort_all():
    arm.sort()
    arm_controller_haha.sort_all_components(arm_controller_haha)
    print("haha")
    return 'Sort all signal received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

