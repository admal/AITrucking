import tensorflow as tf
from config import *

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

class Model:
    _model_graph = None
    _model = None
    model_dir = "C:\\Users\\ASUS\\Documents\\PW\\SieciNeuronowe\\Projekt2\\Model"

    def __init__(self, model_dir = None):
        """
        Initializes model
        :param model_dir: directory with model, it can be trained and used to predict rotation
        or with checkpoints to continue training
        """
        if model_dir is None:
            "C:\\Users\\ASUS\\Documents\\PW\\SieciNeuronowe\\Projekt2\\Model"
        else:
            self.model_dir = model_dir

    def get_model(self):
        if self._model_graph is None:
            self._model_graph = self._build_model()
            self._model = tflearn.DNN(self._model_graph,
                                tensorboard_dir=MODEL_DIRECTORY,
                                tensorboard_verbose=3)

        return self._model

    def _build_model(self):
        network = input_data(shape=[None, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])

        network = conv_2d(
            network,
            nb_filter=24,
            filter_size=5,
            activation='relu')

        network = conv_2d(
            network,
            nb_filter=36,
            filter_size=5,
            activation='relu'
        )

        network = max_pool_2d(
            network,
            2,
            strides=2)

        network = conv_2d(
            network,
            nb_filter=48,
            filter_size=3,
            activation='relu')

        network = conv_2d(
            network,
            nb_filter=64,
            filter_size=3,
            activation='relu'
        )

        network = max_pool_2d(
            network,
            2,
            strides=2)

        network= tflearn.flatten(network)

        network = fully_connected(
            network,
            100,
            activation='relu'
        )
        
        network = tflearn.dropout(
            network,
            keep_prob=0.5    
        )

        network = fully_connected(
            network,
            50,
            activation='relu'
        )
        
        network = tflearn.dropout(
            network,
            keep_prob=0.5    
        )

        network = fully_connected(
            network,
            10,
            activation='relu'
        )
        
        network = tflearn.dropout(
            network,
            keep_prob=0.5    
        )

        network = fully_connected(
            network,
            1,
            activation='linear',
            bias=False
        )
        network = tf.reshape(network, [-1, 1]) #so that accuracy is binary_accuracy

        network = regression(
            network,
            optimizer='SGD',
            learning_rate=LEARNING_RATE,
            loss='mean_square',
            name='targets',
            metric='accuracy'
        )

        return network

    def load(self):
        self.get_model().load(self.model_dir)
