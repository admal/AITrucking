import os
import scipy
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from config import *
import logging

def convert_from_rgb(image):
    return (image / 127.5) - 1.0

def preprocess(image):
    image = convert_from_rgb(image)
    return image


def load_image(img_path):
    image = np.asfarray(Image.open(img_path))  # from PIL image to numpy array
    return image


# Selects picture to be one of the screenshots, left center or right and adjusts angle
def load_picture(ss_paths, steering_angle):
    img_path = ss_paths[0]
    image = load_image(img_path)

    return image, steering_angle


# randomly mirror the image and the steering angle
def random_flip(image, steering_angle):
    if np.random.rand() < 0.5:
        image = np.flip(image, 1)
        steering_angle = -steering_angle
    return image, steering_angle


flipped = 0
delta = 0.2

def flip(image, steering_angle):
    flipped_image = np.flip(image, 1)
    return flipped_image, -steering_angle

# preprocess and augument dataset
def augument(ss_paths, steering_angle, to_flip, flip_to_right):
    global flipped
    global delta

    image, steering_angle = load_picture(ss_paths, steering_angle)

    rnd = np.random.choice(2)

    if flip_to_right and steering_angle < -delta and rnd == 1 and flipped < abs(to_flip):
        image, steering_angle = flip(image, steering_angle)
        flipped = flipped + 1
    elif not flip_to_right and steering_angle > delta and rnd == 1 and flipped < abs(to_flip):
        image, steering_angle = flip(image, steering_angle)
        flipped = flipped + 1

    image = preprocess(image)  # apply the preprocessing    
    image, steering_angle = random_flip(image, steering_angle)

    # todo maybe add translate, shadow, brightness 
    return image, steering_angle


def load_csv_data(learning_set_path, validation_set_size):
    data_df = pd.read_csv(os.path.join(os.getcwd(), learning_set_path, 'train_data.csv'),
                          names=['center', 'steering', 'throttle', 'brake'])

    # yay dataframes, we can select rows and columns by their names
    # we'll store the camera images as our input data
    x = data_df[["center"]].values
    # and our steering commands as our output data
    y = data_df['steering'].values

    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=validation_set_size, random_state=0,
                                                          shuffle=True)

    return (x_train, y_train), (x_valid, y_valid)


def load_batch(ss_paths_set, steering_angles, idx, batch_size):
    global flipped
    global delta
    '''
    input is paths to 3 images and, steering angle
    output is selected and altered image and adjusted steering_angle
    '''
    input_images_batch = []
    steering_angles_batch = []

    
    steering_right = [(angle, idx) for (angle, idx) in zip(steering_angles, range(0, len(steering_angles))) if angle > delta]
    steering_left = [(angle, idx) for (angle, idx) in zip(steering_angles, range(0, len(steering_angles))) if angle < -delta]
    straight = [(angle, idx) for (angle, idx) in zip(steering_angles, range(0, len(steering_angles))) if angle == 0]
    flipped = 0
    to_flip = np.floor((len(steering_right) - len(steering_left)) / 2)
    flip_to_right = to_flip < 0.0

    logging.info('right {}'.format(len(steering_right)))
    logging.info('left {}'.format(len(steering_left)))
    logging.info('straight {}'.format(len(straight)))
    logging.info('to flip {}'.format(to_flip))
    # load images for current iteration
    for ss_paths, steering_angle in zip(ss_paths_set[idx * batch_size:(idx + 1) * batch_size],
                                        steering_angles[idx * batch_size:(idx + 1) * batch_size]):
        image, steering_angle = augument(ss_paths, steering_angle, to_flip, flip_to_right)
        input_images_batch.append(image)
        steering_angles_batch.append(steering_angle)

    steering_right = [(angle, idx) for (angle, idx) in zip(steering_angles_batch, range(0, len(steering_angles_batch))) if angle > 0]
    steering_left = [(angle, idx) for (angle, idx) in zip(steering_angles_batch, range(0, len(steering_angles_batch))) if angle < 0]
    straight = [(angle, idx) for (angle, idx) in zip(steering_angles_batch, range(0, len(steering_angles_batch))) if angle == 0]
    
    logging.info('length {}'.format(len(steering_angles_batch)))
    logging.info('right after {}'.format(len(steering_right)))
    logging.info('left after {}'.format(len(steering_left)))
    logging.info('straight {}'.format(len(straight)))
    logging.info(flipped)

    return input_images_batch, steering_angles_batch
