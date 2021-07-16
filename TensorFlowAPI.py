# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import tensorflow.keras as tf
# Internals
import GUI_subwidgets
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Model:

    def __init__(self, name):
        self.name = name
        self.model = tf.Model()






