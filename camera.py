from picamera import PiCamera
from picamera import array
from time import sleep

res = (240, 240)

def init_camera():
    camera = PiCamera()
    output = array.PiRGBArray(camera)
    camera.rotation = 0
    # Max res for camera (2592, 1944)
    camera.resolution = res
    return camera, output

def get_image(camera, output):
    camera.capture(output, 'rgb')
    return output.array
    

if __name__ == "__main__":
    camera, output = init_camera()
    frame = get_image(camera, output)
    print(frame.shape)
