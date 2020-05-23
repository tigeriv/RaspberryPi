# Motor driver rainbow blue->green ENA, IN1-4, ENB
# Motor 0: enable line A, input 1 & 2
# GPIO 17, 27, 22 = ENA, IN1, IN2
# Motor 1: GPIO 23, 24, 25 = IN3, IN4, ENB
# Both inputs same brakes, opposite spins
# IN1 runs motor backwards, IN2 forwards
# 0 is Right, 1 is Left


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motorR = [17, 27, 22]
motorL = [25, 23, 24]
ENABLE = 0
BACK = 1
FORWARD = 2
motors = [motorL, motorR]

for pin in motorL + motorR:
    GPIO.setup(pin, GPIO.OUT)
    
def forward():
    for motor in motors:
        GPIO.output(motor[ENABLE], True)
        GPIO.output(motor[FORWARD], True)
        GPIO.output(motor[BACK], False)
        
def backward():
    for motor in motors:
        GPIO.output(motor[ENABLE], True)
        GPIO.output(motor[FORWARD], False)
        GPIO.output(motor[BACK], True)

def stop():
    for motor in motors:
        GPIO.output(motor[ENABLE], False)
        GPIO.output(motor[FORWARD], False)
        GPIO.output(motor[BACK], False)

backward()
time.sleep(5)
stop()
forward()
time.sleep(5)
stop()