import numpy as np
import time
import tflite_runtime.interpreter as tflite
from camera import *


def init_model():
    # Load TFLite model and allocate tensors.
    interpreter = tflite.Interpreter(model_path="converted_model.tflite")
    interpreter.allocate_tensors()
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


# Must be shape 1, 240, 240, 3
def get_mask(input_image, interpreter, input_details, output_details):
    input_shape = input_details[0]['shape']
    input_data = input_image.astype('float32')
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    cat_image = np.argmax(output_data[0], axis=-1)
    return cat_image


def center_of_mass(mask):
    points = np.argwhere(mask)
    if len(points) == 0:
        return None
    return np.average(points, axis=0)


if __name__ == "__main__":
    camera, output = init_camera()
    frame = np.asarray([get_image(camera, output)])
    interpreter, input_details, output_details = init_model()
    mask = get_mask(frame, interpreter, input_details, output_details)
    road_image = cat_to_im(mask)
    save_image("OG.jpg", frame[0])
    save_image("Mask.jpg", road_image)
    print(center_of_mass(mask))
