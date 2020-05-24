# Simple PID controller
from RunLite import *
from motor import *
from camera import *
import math
import time

KP = 1
KI = 1
last_ten = [[0.0, 0.0]] * 30
ten_sum = np.sum(np.asarray(last_ten), axis=0)


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
        frame = np.asarray([get_image(camera, output)])
        mask = get_mask(frame, interpreter, input_details, output_details)
        com = center_of_mass(mask)
        if com is None:
            power, angle = 0, 0
        else:
            power, angle = com_to_loss(com, (240, 240))
            power = 0.9 + (0.2 * power)
        
        i_avg = calculate_integral([power, angle])
        controls = np.asarray([power, angle])
        print(i_avg)
        controls = (KP * controls + KI * i_avg) / (KP + KI)
        # atan returns a number, -pi/2 to pi/2
        power = controls[0]
        angle = controls[1]
        
        if angle < -0.5:
            angle =  -0.5
            power = 1
        if angle > 0.5:
            angle = 0.5
            power = 1
            
        print(power, angle)
        steer(power, angle)
        
