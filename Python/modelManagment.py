import pandas as pd
import numpy as np
import tensorflow as tf


class Model:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model(model_path)

    def load_model(model_path):
        """
        Load a model from a given path
        :param model_path: Path to the model
        :return: The loaded model
        """
        return tf.keras.models.load_model(model_path)


    def runModel(input, self):
        """
        Run a model with a given input
        :param input: The input for the model
        :return: The output of the model
        """
        return self.model.predict(input)
    
