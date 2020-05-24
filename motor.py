# Motor driver rainbow blue->green ENA, IN1-4, ENB
# Motor 0: enable line A, input 1 & 2
# GPIO 17, 27, 22 = ENA, IN1, IN2
# Motor 1: GPIO 23, 24, 25 = IN3, IN4, ENB
# Both inputs same brakes, opposite spins
# IN1 runs motor backwards, IN2 forwards
# 0 is Right, 1 is Left

# Note, you need to install wiring pi with pip3 install wiringpi


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
# This constant is used when calculating duty cycle
# R is more powerful than L
RPOWER = 0.87

    
def forward():
    wiringpi.softPwmWrite(motorL[ENABLE], 100)
    wiringpi.softPwmWrite(motorR[ENABLE], 87)
    for motor in motors:
        # GPIO.output(motor[ENABLE], True)
        GPIO.output(motor[FORWARD], True)
        GPIO.output(motor[BACK], False)
      
      
def backward():
    wiringpi.softPwmWrite(motorL[ENABLE], 100)
    wiringpi.softPwmWrite(motorR[ENABLE], 87)
    for motor in motors:
        # GPIO.output(motor[ENABLE], True)
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
    
    
# A 2-item tuple. 1st is the center of mass row, 2nd is column
# Returns values in range -0.5 to 0.5, where 0 is optimal
# Higher means faster for distance, positive angle is right (so steer to the left)
def com_to_loss(com, res):
    distance = (res[0]/2 - com[0]) / res[0]
    angle = (com[1] - res[1]/2) / res[1]
    return distance, angle


def move_motor(motor, power):
    wiringpi.softPwmWrite(motor[ENABLE], power)
    GPIO.output(motor[FORWARD], True)
    GPIO.output(motor[BACK], False)


# L is negative, R is positive
def steer(power, angle):
    print(power, angle)
    RPower = 100 * power * RPOWER
    LPower = 100 * power

    # Greater than 0: decrease R
    if angle > 0:
        RPower *= abs(1 - angle)
    # Less than 0: decrease L
    else:
        LPower *= abs(1 - angle)

    move_motor(motorL, int(LPower))
    move_motor(motorR, int(RPower))
    
    
if __name__ == "__main__":
    init_motors()

    forward()
    time.sleep(2)
    stop()
    backward()
    time.sleep(2)
    stop()
