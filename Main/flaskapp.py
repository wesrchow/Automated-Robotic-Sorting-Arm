from flask import Flask
from testing import SortingArm
from calibrate import calibrate_run

app = Flask(__name__)
arm = SortingArm()
calibrate_1 = calibrate_run

@app.route('/calibrate')
def calibrate():
    arm.calibrate_arm()
    calibrate_1.run_calibrate()
    return 'Calibration signal received'

@app.route('/sort-all')
def sort_all():
    arm.sort()
    return 'Sort all signal received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

