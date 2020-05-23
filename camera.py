from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 0
# Max res for camera (2592, 1944)
camera.resolution = (240, 240)
camera.framerate = 15

camera.start_preview()
# camera.start_recording('/home/pi/Desktop/video.h264')
for i in range(60):
    sleep(1)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
# camera.stop_recording()
camera.stop_preview()
