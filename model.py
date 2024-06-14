#model
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2

interpreter = tflite.Interpreter(model_path="/home/smartFarm/Desktop/project_final/model/model.tfliteQuant")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details= interpreter.get_output_details()

def modelrun(image_path):
    #image_path = "/home/smartFarm/Desktop/project/image_store/test.jpeg"
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.expand_dims(resized_image, axis=0)
    input_data = input_data.astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    with open("/home/smartFarm/Desktop/project_final/model/labels.txt", "r") as f:
        labels = f.read().splitlines()
    predicted_label = labels[np.argmax(output_data)]
    return predicted_label
