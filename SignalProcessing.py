# -*- coding: utf-8 -*-

"""This module contains methods that process signals. Note that the input signal is assumed to be of the type
SignalSystem.TimeSignal(). The methods will usually also return a signal of the same type."""

# standard library
import logging
import random
# 3rd party
import numpy as np
# Internals
import Signals as ss
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def FFT(signal):
    """Recover the **Fast Fourier Transform** (FFT) of the signal **Y** on the time domain **T**."""
    Y_f = np.fft.fft(signal.Y)[:signal.n // 2]
    X_f = np.fft.fftfreq(n=signal.n, d=1 / signal.f_a)[:signal.n // 2]
    F_signal = ss.TimeSignal.from_data(X_f, Y_f)
    return F_signal


def MagnitudeFFT(signal):
    """Recover the **Fast Fourier Transform** (FFT) of the signal **Y** on the time domain **T**."""
    FFT_signal= FFT(signal)
    Magnitude_signal = ss.TimeSignal.from_data(FFT_signal.X, np.absolute(FFT_signal.Y))
    return Magnitude_signal


def add_gaussian_noise(signal, mu, sigma):
    for k, y in enumerate(signal.Y):
        signal.Y[k] += random.gauss(mu, sigma)



