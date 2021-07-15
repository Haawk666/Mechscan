# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ColorPreview(QtWidgets.QFrame):

    def __init__(self, *args, r=0, g=0, b=0, a=255):
        super().__init__(*args)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setMaximumWidth(40)
        self.setMinimumWidth(40)
        self.setStyleSheet('background-color: rgb({}, {}, {})'.format(self.r, self.g, self.b))

    def set_color(self, r, g, b, a):

        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.setStyleSheet('background-color: rgb({}, {}, {})'.format(self.r, self.g, self.b))


