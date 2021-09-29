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


def custom_R(x, string='x'):
    """Custom function as string"""
    return eval(string)


def custom_R2(x_1, x_2, string='x_1 + x_2'):
    """Custom function as string"""
    return eval(string)


def sine_RR(x, A=666.0, f=666.0, phi=0.0):
    """The sine function from R to R."""
    return A * np.sin(2 * np.pi * f * (x - phi))


def sine_RC(x, A=666.0, f=666.0, phi=0.0):
    """The sine function from R to C."""
    return A * np.exp(-2 * np.pi * f * (x - phi) * 1j)


def cosine_RR(x, A=666.0, f=666.0, phi=0.0):
    """The cosine function from R to R."""
    return A * np.cos(2 * np.pi * f * (x - phi))


def cosine_RC(x, A=666.0, f=666.0, phi=0.0):
    """The cosine function from R to C."""
    return A * np.exp(2 * np.pi * f * (x - phi) * 1j)


def gauss_RR(x, A=1, mu=0.0, sigma=1.0):
    """The gauss curve with amplitude A from R to R"""
    return A * np.exp(- 0.5 * ((x - mu) / sigma) ** 2)


def gauss_RC(x, A=1, mu=0.0, sigma=1.0):
    """The gauss curve with amplitude A from R to C"""
    return A * (np.exp(- 0.5 * ((x - mu) / sigma) ** 2) + np.exp(- 0.5 * ((x - mu) / sigma) ** 2) * 1j)


def linear_chirp_RR(x, A=666.0, x_0=0.0, x_1=1.0, f_0=0.0, f_1=666.0):
    """Linear chirp starting with frequency f_0 at x_0 and extends to frequency f_1 at x_1. R to R"""
    return A * np.sin(2 * np.pi * (((f_1 - f_0) / (x_1 - x_0)) * x + f_0 - ((f_1 - f_0) / (x_1 - x_0)) * x_0) * x)


def morlet_wavelet_RR(x, A=666.0, mu=0.0, sigma=1.0, f=666.0, phi=0.0):
    """Morlet wavelet from R to R"""
    return A * np.exp(- 0.5 * ((x - mu) / sigma) ** 2) * np.cos(2 * np.pi * f * (x - phi))


def morlet_wavelet_RC(x, A=666.0, mu=0.0, sigma=1.0, f=666.0, phi=0.0):
    """Morlet wavelet from R to C"""
    return A * np.exp(- 0.5 * ((x - mu) / sigma) ** 2 + 2 * np.pi * f * (x - phi) * 1j)


def get_function_map(signal):

    if signal.dimensions == 1:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = {
                'custom': {
                    'args': ['x'],
                    'kwargs': dict(),
                    'function': custom_R,
                    'vector': True
                },
                'sine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': sine_RR,
                    'vector': True
                },
                'cosine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': cosine_RR,
                    'vector': True
                },
                'pulse': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                    },
                    'function': gauss_RR,
                    'vector': True
                },
                'linear chirp': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'x_0': Parameter(signal.x_start, signal.x_end, 1.0, 2, signal.x_start),
                        'x_1': Parameter(signal.x_start, signal.x_end, 1.0, 2, signal.x_end),
                        'f_0': Parameter(0.0, 10000.0, 10.0, 1, 0.0),
                        'f_1': Parameter(0.0, 10000.0, 10.0, 1, 666.0)
                    },
                    'function': linear_chirp_RR,
                    'vector': True
                },
                'morlet wavelet': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0)
                    },
                    'function': morlet_wavelet_RR,
                    'vector': True
                }
            }

        else:

            functions = {
                'custom': {
                    'args': ['x'],
                    'kwargs': dict(),
                    'function': custom_R,
                    'vector': True
                },
                'sine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': sine_RC,
                    'vector': True
                },
                'cosine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': cosine_RC,
                    'vector': True
                },
                'complex morlet wavelet': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0)
                    },
                    'function': morlet_wavelet_RC,
                    'vector': True
                },
                'pulse': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                    },
                    'function': gauss_RC,
                    'vector': True
                }
            }

    elif signal.dimensions == 2:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = {
                'custom': {
                    'args': ['x_1', 'x_2'],
                    'kwargs': dict(),
                    'function': custom_R2,
                    'vector': False
                }
            }

        else:

            functions = {
                'custom': {
                    'args': ['x_1', 'x_2'],
                    'kwargs': dict(),
                    'function': custom_R2,
                    'vector': False
                }
            }

    else:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = dict()

        else:

            functions = dict()

    return functions


class Parameter:

    def __init__(self, min, max, step, dec, default, value=None):

        self.min = min
        self.max = max
        self.step = step
        self.dec = dec
        self.default = default
        if value is None:
            self.value = self.default
        else:
            self.value = value

