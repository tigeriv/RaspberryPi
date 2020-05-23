# Motor driver rainbow blue->green ENA, IN1-4, ENB
# Motor 0: enable line A, input 1 & 2
# GPIO 17, 27, 22 = ENA, IN1, IN2
# Motor 1: GPIO 23, 24, 25 = IN3, IN4, ENB
# Both inputs same brakes, opposite spins
# IN1 runs motor backwards, IN2 forwards
# 0 is Right, 1 is Left


import RPi.GPIO as GPIO
import time
import wiringpi

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

OUTPUT = 1

motorR = [17, 27, 22]
motorL = [25, 23, 24]
ENABLE = 0
BACK = 1
FORWARD = 2
motors = [motorL, motorR]

    
def forward():
    for motor in motors:
        # GPIO.output(motor[ENABLE], True)
        wiringpi.softPwmWrite(motor[ENABLE], 100)
        GPIO.output(motor[FORWARD], True)
        GPIO.output(motor[BACK], False)
      
      
def backward():
    for motor in motors:
        # GPIO.output(motor[ENABLE], True)
        wiringpi.softPwmWrite(motor[ENABLE], 50)
        GPIO.output(motor[FORWARD], False)
        GPIO.output(motor[BACK], True)

def stop():
    for motor in motors:
        # GPIO.output(motor[ENABLE], False)
        wiringpi.softPwmWrite(motor[ENABLE], 0)
        GPIO.output(motor[FORWARD], False)
        GPIO.output(motor[BACK], False)
    

def init_motors():
    for pin in motorL + motorR:
        GPIO.setup(pin, GPIO.OUT)
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(motorL[ENABLE], OUTPUT)
    wiringpi.pinMode(motorR[ENABLE], OUTPUT)
    wiringpi.softPwmCreate(motorL[ENABLE], 0, 100)
    wiringpi.softPwmCreate(motorR[ENABLE], 0, 100)
        
    
init_motors()

forward()
time.sleep(1)
stop()
backward()
time.sleep(1)
stop()