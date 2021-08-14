# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import random
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
import wave
import h5py
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemInterface(QtWidgets.QWidget):

    def __init__(self, *args, system=None):
        super().__init__(*args)

        self.signal = system

        self.build_layout()
        self.update_info()

    def build_layout(self):
        pass

    def update_info(self):
        pass










