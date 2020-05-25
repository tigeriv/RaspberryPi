# Simple PID controller
from RunLite import *
from motor import *
from camera import *
import math
import time

KP = 1
KI = 0
KD = 0
last_ten = [[0.0, 0.0]] * 10
ten_sum = np.sum(np.asarray(last_ten), axis=0)
MID_POWER = 0.8
MAX_ANGLE = 0.5


def calculate_integral(new_term):
    global last_ten
    global ten_sum
    last_ten.append(new_term)
    ten_sum += new_term
    ten_sum -= last_ten.pop(0)
    i_avg = np.sum(np.asarray(last_ten), axis=0) / len(last_ten)
    return i_avg


if __name__ == "__main__":
    camera, output = init_camera()
    interpreter, input_details, output_details = init_model()
    init_motors()

    while True:
        last_angle = 0
        
        frame = np.asarray([get_image(camera, output)])
        mask = get_mask(frame, interpreter, input_details, output_details)
        com = center_of_mass(mask)
        if com is None:
            power, angle = 0, 0
        else:
            power, angle = com_to_loss(com, (240, 240))
            power = MID_POWER + (0.2 * power)
            
        # Positive: right, negative: left
        d_angle = angle - last_angle
        d_controls = np.asarray([MID_POWER, d_angle])
        
        i_avg = calculate_integral([power, angle])
        controls = np.asarray([power, angle])
        controls = (KP * controls + KI * i_avg + KD * d_controls) / (KP + KI + KD)
        # atan returns a number, -pi/2 to pi/2
        power = controls[0]
        angle = controls[1]
        
        if angle < -MAX_ANGLE:
            angle =  -MAX_ANGLE
            power = MID_POWER
        if angle > MAX_ANGLE:
            angle = MAX_ANGLE
            power = MID_POWER
            
        print(power, angle)
        steer(power, angle)
        
        time.sleep(0.5)
        steer(0, 0)
        
        
