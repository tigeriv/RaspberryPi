from picamera import PiCamera
from picamera import array
from time import sleep
import imageio
import numpy as np

res = (240, 240)
cat_to_color = {0: (0, 0, 0), 1: (0, 0, 255)}

def init_camera():
    camera = PiCamera()
    output = array.PiRGBArray(camera)
    camera.rotation = 0
    # Max res for camera (2592, 1944)
    camera.resolution = res
    sleep(5)
    return camera, output


def get_image(camera, output):
    output.truncate(0)
    camera.capture(output, 'rgb')
    return output.array


def cat_to_im(image):
    new_image = np.zeros((len(image), len(image[0]), 3), dtype=np.int32)
    for row_num in range(len(image)):
        for ind_num in range(len(image[row_num])):
            category = image[row_num][ind_num]
            new_image[row_num, ind_num] = cat_to_color[category]
    return new_image


# Saves a numpy array as an image
def save_image(path, img):
    imageio.imwrite(path, img)
    

if __name__ == "__main__":
    camera, output = init_camera()
    frame = get_image(camera, output)
    print(frame.shape)
