# -*- coding: utf-8 -*-

"""Module docstring"""

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


def fft(time_signal):
    """Recover the **Fast Fourier Transform** (FFT) of the signal **Y** on the time domain **T**."""
    if time_signal.bit_depth in [1, 2, 8, 16, 32]:
        bit_depth = 64
    else:
        bit_depth = 128
    Y_f = np.fft.fftshift(np.fft.fft(time_signal.Y, axis=0)).astype(eval('np.complex{}'.format(bit_depth)))
    X_f = np.linspace(-time_signal.f_s / 2.0, time_signal.f_s / 2.0, num=Y_f.shape[0], dtype=np.float64)
    frequency_signal = ss.FrequencySignal.from_data(X_f, Y_f)
    frequency_signal.time_signal = time_signal
    return frequency_signal


def ifft(frequency_signal):
    f_s = 2.0 * (frequency_signal.X[-1])
    delta_x = 1.0 / f_s

    Y = np.fft.ifft(np.fft.ifftshift(frequency_signal.Y), axis=0).real

    if frequency_signal.time_signal is not None:
        x_start = frequency_signal.time_signal.X[0]
        x_end = frequency_signal.time_signal.X[-1]
        bit_depth = frequency_signal.time_signal.bit_depth
    else:
        x_start = 0.0
        x_end = delta_x * (frequency_signal.n - 1)
        if frequency_signal.bit_depth == 128:
            bit_depth = 64
        elif frequency_signal.bit_depth == 64:
            bit_depth = 16
        else:
            bit_depth = 8 * Y.dtype.itemsize

    time_signal = ss.TimeSignal(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain='int', channels=frequency_signal.channels)
    time_signal.Y = Y.astype(time_signal.Y.dtype)
    return time_signal


def gabor_transform(time_signal, window_size=1.0, window_function='Hann'):
    N = int(np.round(window_size / time_signal.delta_x + 1.0, decimals=0))
    X = np.linspace(0.0, window_size, num=N, dtype=np.float64)
    window_function_values = np.ndarray((N, time_signal.channels), dtype=np.float64)
    if window_function == 'Hann':
        for x in range(N):
            window_function_values[x] = (np.sin(np.pi * x / N)) ** 2
    else:
        for x in range(N):
            window_function_values[x] = (np.sin(np.pi * x / N)) ** 2



    time_signal = ss.TimeSignal.from_data(X, window_function_values)
    return time_signal





