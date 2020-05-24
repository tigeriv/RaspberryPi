# Simple PID controller
from RunLite import *
from motor import *
from camera import *
import math
import time

KP = 1


if __name__ == "__main__":
    camera, output = init_camera()
    interpreter, input_details, output_details = init_model()
    init_motors()

    while True:
        frame = np.asarray([get_image(camera, output)])
        mask = get_mask(frame, interpreter, input_details, output_details)
        com = center_of_mass(mask)
        if com is None:
            continue
        power, angle = com_to_loss(com, (240, 240))

        # atan returns a number, -pi/2 to pi/2
        power = 0.75 + 0.25 * math.atan(power * KP) / (math.pi / 2)
        steer(power, angle)
        
