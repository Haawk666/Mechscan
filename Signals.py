# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import scipy.fft
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import TensorFlowAPI as tf
import DataManager
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def FFT(Y, n, f_a, T):
    """Recover the **Fast Fourier Transform** (FFT) of the signal **Y** on the time domain **T**."""
    Omega = scipy.fft.fftfreq(Y.shape[0], T)[n//2:]
    return Omega, np.absolute(scipy.fft.fft(Y))[n//2:]

