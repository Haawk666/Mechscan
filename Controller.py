# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import numpy as np
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Controller:

    def __init__(self, gui_obj):

        self.GUI = gui_obj
        self.data = None

    def load_data(self, path_string):
        pass
