# Simple PID controller
from RunLite import *
from motor import *
from camera import *
import math

KP = 10


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
        print(com)
        power, angle = com_to_loss(com, (240, 240))
        power = math.atan(power * KP) / (math.pi / 2)
        steer(power, angle)
        
