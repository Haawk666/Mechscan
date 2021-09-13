# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import numpy as np
# Internals
import Signal as ss
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def evaluate(signal, function, method='overwrite', a=None, b=None, channels=None, update=None):
    """Assumes that the function output matches the signal type!"""

    if channels is None:
        channels = [x for x in range(signal.channels)]

    if a is None:
        if signal.dimensions == 1:
            a = [signal.x_start]
        else:
            a = []
            for d in range(signal.dimensions):
                a.append(signal.x_start[d])

    if b is None:
        if signal.dimensions == 1:
            b = [signal.x_end]
        else:
            b = []
            for d in range(signal.dimensions):
                b.append(signal.x_end[d])

    a_index = [0] * signal.dimensions
    if signal.dimensions == 1:
        b_index = [signal.n - 1]
    else:
        b_index = [x for x in signal.n]
        b_index -= [1] * signal.dimensions

    if signal.dimensions == 1:
        distance_a = 100000000000
        distance_b = 100000000000
        for k, x in enumerate(signal.X):
            if np.absolute(a[0] - x) < distance_a:
                distance_a = np.absolute(a[0] - x)
                a_index[0] = k
            if np.absolute(b[0] - x) < distance_b:
                distance_b = np.absolute(b[0] - x)
                b_index[0] = k
    else:
        distance_a = []
        distance_b = []
        for d in range(signal.dimensions):
            distance_a.append(100000000000)
            distance_b.append(100000000000)
            for k, x in enumerate(signal.X[d]):
                if np.absolute(a[d] - x) < distance_a[d]:
                    distance_a[d] = np.absolute(a[d] - x)
                    a_index[d] = k
                if np.absolute(b[0] - x) < distance_b[d]:
                    distance_b[d] = np.absolute(b[d] - x)
                    b_index[d] = k

    if signal.dimensions == 1:

        values = np.zeros((signal.Y.shape[0]), dtype=signal.Y.dtype)

        for k in range(signal.n):
            values[k] = function(signal.X[k])
            if update is not None:
                update.setValue(k)

        for channel in channels:

            if method == 'overwrite':
                signal.Y[a_index[0]:b_index[0], channel] = values.astype(eval(signal.valid_types[signal.type_id]))[a_index[0]:b_index[0]]

            elif method == 'add':
                signal.Y[a_index[0]:b_index[0], channel] += values.astype(eval(signal.valid_types[signal.type_id]))[a_index[0]:b_index[0]]

            elif method == 'multiply':
                signal.Y[a_index[0]:b_index[0], channel] = np.multiply(signal.Y[:, channel], values.astype(eval(signal.valid_types[signal.type_id])))[a_index[0]:b_index[0]]

            else:
                raise Exception('Unknown method type')

    elif signal.dimensions == 2:

        values = np.zeros((signal.Y.shape[0], signal.Y.shape[1]), dtype=signal.Y.dtype)

        for i in range(signal.n[0]):
            for j in range(signal.n[1]):

                values[i, j] = function(signal.X[0][i], signal.X[1][j])
                if update is not None:
                    update.setValue(i * j)

        for channel in channels:

            if method == 'overwrite':
                signal.Y[a_index[0]:b_index[0], a_index[1]:b_index[1], channel] = values.astype(eval(signal.valid_types[signal.type_id]))[a_index[0]:b_index[0], a_index[1]:b_index[1]]

            elif method == 'add':
                signal.Y[a_index[0]:b_index[0], a_index[1]:b_index[1], channel] += values.astype(eval(signal.valid_types[signal.type_id]))[a_index[0]:b_index[0], a_index[1]:b_index[1]]

            elif method == 'multiply':
                signal.Y[a_index[0]:b_index[0], a_index[1]:b_index[1], channel] = np.multiply(signal.Y[:, :, channel], values.astype(eval(signal.valid_types[signal.type_id])))[a_index[0]:b_index[0], a_index[1]:b_index[1]]

            else:
                raise Exception('Unknown method type')

    else:

        raise Exception('Not implemented!')

    return signal


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


def gabor_transform(time_signal, window_size=0.1, window_function='Hann', delta_tau=None, delta_freq=None, update=None):

    if time_signal.bit_depth in [1, 2, 8, 16, 32]:
        bit_depth = 64
    else:
        bit_depth = 128

    if delta_tau is None:
        delta_tau = time_signal.delta_x
    if delta_freq is None:
        delta_freq = (time_signal.X[-1] - time_signal.X[0]) / (time_signal.n - 1.0)

    # transform params:
    alpha_n = int(2 * np.round(window_size / time_signal.delta_x + 1, decimals=0) + 1)
    delta_tau_n = int(np.round(delta_tau / time_signal.delta_x, decimals=0))
    delta_f_n = int(np.round(time_signal.f_s / delta_freq + 1, decimals=0))
    delta_o_n = alpha_n - delta_tau_n
    delta_o = time_signal.delta_x * (delta_o_n - 1)
    P_n = int(np.round(window_size / time_signal.delta_x + 1, decimals=0))

    window_function_values = np.zeros((alpha_n, ), dtype=np.float64)
    if window_function == 'Hann':
        for x in range(alpha_n):
            window_function_values[x] = (np.sin(np.pi * x / alpha_n)) ** 2
    else:
        for x in range(alpha_n):
            window_function_values[x] = (np.sin(np.pi * x / alpha_n)) ** 2

    # Transform sample space:
    x_start = [time_signal.X[0], -time_signal.f_s / 2]
    x_end = [time_signal.X[0] + delta_tau_n * time_signal.delta_x * (np.round(time_signal.N / delta_tau_n, decimals=0) - 1), time_signal.f_s / 2]
    delta_x = [delta_tau_n * time_signal.delta_x, time_signal.f_s / np.round(time_signal.f_s / delta_freq, decimals=0)]
    f_s = [1 / delta_x[0], 1 / delta_x[1]]
    N = [int(np.round(time_signal.N / delta_tau_n, decimals=0)), int(np.round(time_signal.f_s / delta_freq + 1, decimals=0))]

    tau = np.linspace(x_start[0], x_end[0], num=N[0], dtype=np.float64)
    freq = np.linspace(x_start[1], x_end[1], num=N[1], dtype=np.float64)

    Y_g = np.zeros((tau.shape[0], freq.shape[0], time_signal.channels), dtype=eval('np.complex{}'.format(bit_depth)))

    Y = time_signal.Y
    Y = np.concatenate((np.zeros((P_n, time_signal.channels), dtype=Y.dtype), Y, np.zeros((P_n, time_signal.channels), dtype=Y.dtype)), axis=0)

    for channel in range(time_signal.channels):

        for i in range(N[0]):

            k = i * delta_tau_n
            Y_g[i, :, channel] = np.fft.fftshift(np.fft.fft(Y[k:(k + alpha_n), channel] * window_function_values, n=N[1], axis=0)).astype(eval('np.complex{}'.format(bit_depth)))
            if update is not None:
                update.setValue(channel * N[0] + i)

    time_frequency_signal = ss.TimeFrequencySignal.from_data([tau, freq], Y_g)
    time_frequency_signal.time_signal = time_signal

    report = {
        'alpha_n': alpha_n,
        'delta_tau_n': delta_tau_n,
        'delta_f_n': delta_f_n,
        'delta_o_n': delta_o_n,
        'delta_o': delta_o,
        'P_n': P_n
    }

    for key, value in report.items():
        print('{}: {}'.format(key, value))

    return time_frequency_signal


def inverse_gabor_transform(time_frequency_signal, window_size=1.0, window_function='Hann', delta_tau=None, delta_freq=None):
    pass


def wavelet_transform(time_signal, window_size=1.0, window_function='Morlet', delta_tau=None, delta_freq=None):

    if time_signal.bit_depth in [1, 2, 8, 16, 32]:
        bit_depth = 64
    else:
        bit_depth = 128

    if delta_tau is None:
        delta_tau = time_signal.delta_x
    if delta_freq is None:
        delta_freq = (time_signal.X[-1] - time_signal.X[0]) / (time_signal.n - 1.0)

    # transform params:
    alpha_n = int(2 * np.round(window_size / time_signal.delta_x + 1, decimals=0) + 1)
    delta_tau_n = int(np.round(delta_tau / time_signal.delta_x, decimals=0))
    delta_f_n = int(np.round(time_signal.f_s / delta_freq + 1, decimals=0))
    delta_o_n = alpha_n - delta_tau_n
    delta_o = time_signal.delta_x * (delta_o_n - 1)
    P_n = int(np.round(window_size / time_signal.delta_x + 1, decimals=0))

    f = 20.0
    sigma = 0.2 * window_size

    window_function_values = np.zeros((alpha_n,), dtype=np.complex128)
    if window_function == 'Morlet':
        for x in range(alpha_n):
            window_function_values[x] = np.exp(np.complex(-0.5 * (x / sigma) ** 2), 2 * np.pi * f * x)
    else:
        for x in range(alpha_n):
            window_function_values[x] = np.exp(np.complex(-0.5 * (x / sigma) ** 2), 2 * np.pi * f * x)

    X = np.linspace(0.0, time_signal.delta_x * (alpha_n - 1), num=alpha_n, dtype=np.float64)

    morlet_wavelet = ss.TimeSignal.from_data(X, window_function_values)

    # # Transform sample space:
    # x_start = [time_signal.X[0], -time_signal.f_s / 2]
    # x_end = [
    #     time_signal.X[0] + delta_tau_n * time_signal.delta_x * (np.round(time_signal.N / delta_tau_n, decimals=0) - 1),
    #     time_signal.f_s / 2]
    # delta_x = [delta_tau_n * time_signal.delta_x, time_signal.f_s / np.round(time_signal.f_s / delta_freq, decimals=0)]
    # f_s = [1 / delta_x[0], 1 / delta_x[1]]
    # N = [int(np.round(time_signal.N / delta_tau_n, decimals=0)),
    #      int(np.round(time_signal.f_s / delta_freq + 1, decimals=0))]
    #
    # tau = np.linspace(x_start[0], x_end[0], num=N[0], dtype=np.float64)
    # freq = np.linspace(x_start[1], x_end[1], num=N[1], dtype=np.float64)
    #
    # Y_g = np.zeros((tau.shape[0], freq.shape[0], time_signal.channels), dtype=eval('np.complex{}'.format(bit_depth)))
    #
    # Y = time_signal.Y
    # Y = np.concatenate(
    #     (np.zeros((P_n, time_signal.channels), dtype=Y.dtype), Y, np.zeros((P_n, time_signal.channels), dtype=Y.dtype)),
    #     axis=0)
    #
    # for channel in range(time_signal.channels):
    #
    #     for i in range(N[0]):
    #         k = i * delta_tau_n
    #         Y_g[i, :, channel] = np.fft.fftshift(
    #             np.fft.fft(Y[k:(k + alpha_n), channel] * window_function_values, n=N[1], axis=0)).astype(
    #             eval('np.complex{}'.format(bit_depth)))
    #
    # time_frequency_signal = ss.TimeFrequencySignal.from_data([tau, freq], Y_g)
    # time_frequency_signal.time_signal = time_signal
    #
    # report = {
    #     'alpha_n': alpha_n,
    #     'delta_tau_n': delta_tau_n,
    #     'delta_f_n': delta_f_n,
    #     'delta_o_n': delta_o_n,
    #     'delta_o': delta_o,
    #     'P_n': P_n
    # }
    #
    # for key, value in report.items():
    #     print('{}: {}'.format(key, value))

    return morlet_wavelet




