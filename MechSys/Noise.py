# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
# 3rd party
import numpy as np
# Internals
import Signal_processing
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def noise(signal, noise_gen):
    f = np.fft.fftfreq(len(noise_gen))
    f_spectrum = Signal_processing.fft(signal)
    for k, disturbance in enumerate(noise_gen):
        print(k)
        if not k == 0:
            f_spectrum.Y[k] += disturbance
            f_spectrum.Y[-k] += disturbance


def noise_psd(N, psd=lambda f: 1):
    X_white = np.fft.rfft(np.random.randn(N))
    S = psd(np.fft.rfftfreq(N))
    # Normalize S
    S = S / np.sqrt(np.mean(S ** 2))
    X_shaped = X_white * S
    return np.fft.irfft(X_shaped)


def PSDGenerator(f):
    return lambda N: noise_psd(N, f)


@PSDGenerator
def white_noise(f):
    return 1


@PSDGenerator
def blue_noise(f):
    return np.sqrt(f)


@PSDGenerator
def violet_noise(f):
    return f


@PSDGenerator
def brownian_noise(f):
    return 1 / np.where(f == 0, float('inf'), f)


@PSDGenerator
def pink_noise(f):
    return 1 / np.where(f == 0, float('inf'), np.sqrt(f))




