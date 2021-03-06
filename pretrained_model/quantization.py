import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

root_dir = "../image"

file_name = 'training_model/inference_model_0.993.h5'

def data_generator():
    for file in os.listdir(root_dir):
        img = plt.imread(os.path.join(root_dir, file), format='rgb').astype('float32')
        img = (img.astype('float32') - 127.5) / 128.0
        yield [img[np.newaxis, :, :, :]]


if __name__ == "__main__":

    converter = tf.compat.v1.lite.TFLiteConverter.from_keras_model_file(file_name)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = data_generator
    converter.experimental_new_converter = False
    converter.experimental_new_quantizer = False
    # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    # converter.inference_input_type = tf.uint8
    # converter.inference_output_type = tf.uint8
    tflite_quant_model = converter.convert()

    # write to file
    with open(file_name.split('.')[0]+'_quant.tflite', "wb") as f:
        f.write(tflite_quant_model)