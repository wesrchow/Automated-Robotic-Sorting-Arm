from flask import Flask
from testing import SortingArm

app = Flask(__name__)
arm = SortingArm()

@app.route('/calibrate')
def calibrate():
    arm.calibrate_arm()
    return 'Calibration signal received'

@app.route('/sort-all')
def sort_all():
    arm.sort()
    return 'Sort all signal received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
