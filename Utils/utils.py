import os

import pandas as pd
import numpy as np
from PIL import Image


def load_image(img_path):
	image = np.asfarray(Image.open(img_path))  # from PIL image to numpy array
	return image


def load_csv_data(learning_set_path, validation_set_size):
	train_data_df = pd.read_csv(os.path.join(os.getcwd(), learning_set_path, 'train_data.csv'),
	                            names=['file', 'steering', 'throttle', 'brake'])
	validation_data_df = pd.read_csv(os.path.join(os.getcwd(), learning_set_path, 'validation_data.csv'),
	                                 names=['file', 'steering', 'throttle', 'brake'])

	x_train = train_data_df['file'].values
	y_train = train_data_df['steering'].values

	x_valid = validation_data_df['file'].values
	y_valid = validation_data_df['steering'].values

	return (x_train, y_train), (x_valid, y_valid)


def load_batch(ss_paths_set, steering_angles, idx, batch_size):
	input_images_batch = []
	steering_angles_batch = []

	# load images for current iteration
	for ss_paths, steering_angle in zip(ss_paths_set[idx * batch_size:(idx + 1) * batch_size],
	                                    steering_angles[idx * batch_size:(idx + 1) * batch_size]):
		image= load_image(ss_paths)
		image = (image / 127.5) - 1.0
		input_images_batch.append(image)
		steering_angles_batch.append(steering_angle)

	return input_images_batch, steering_angles_batch
