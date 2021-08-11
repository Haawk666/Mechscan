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


class TimeSignal:

    def __init__(self, t_start=0.0, t_end=10.0, sampling_rate=44000.0):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        self.f_a = sampling_rate  # Sampling rate
        self.t_start = t_start  # Timestamp signal start
        self.t_end = t_end  # Timestamp signal end

        self.T = 1 / self.f_a  # Sampling interval
        self.omega_a = 2 * np.pi / self.T  # Angular sampling frequency
        self.n = int(((self.t_end - self.t_start) / self.T) - 1.0)  # Number of samples

        self.X = np.linspace(self.t_start, self.t_end, num=self.n)  # Discrete time
        self.Y = np.zeros((1, self.n), dtype=float)  # Signal amplitude

    def generate(self, function):
        """Generate signal from function which must be vectorized"""
        self.Y = function(self.X)

