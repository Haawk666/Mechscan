# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
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

