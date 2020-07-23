from time import sleep
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

panmaxRange = 170
tiltmaxRange = 130
finalAngle = 90
sleepTime = 0.04


tiltServo = kit.servo[0]
panServo = kit.servo[1]

tiltServo.set_pulse_width_range(500, 2500)
tiltServo.actuation_range = 180

# https://www.cysmodel.com/products/cys-s3006-6kg-analog-plastic-gear-servo-standard-size/
panServo.set_pulse_width_range(1000, 2000)
panServo.actuation_range = 180



panServo.angle = tiltmaxRange
for i in range(panmaxRange):
    tiltServo.angle = i
    sleep(sleepTime)

for i in range(panmaxRange):
    tiltServo.angle = panmaxRange - i
    sleep(sleepTime)
tiltServo.angle = finalAngle


for i in range(tiltmaxRange):
    panServo.angle = i
    sleep(sleepTime)
for i in range(tiltmaxRange):
    panServo.angle = tiltmaxRange - i
    sleep(sleepTime)
panServo.angle = finalAngle


