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
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def simulate(system):

    # Pad input signals
    x_start = None
    x_end = None
    for s, input_signal in enumerate(system.input_signals):
        if s == 0:
            x_start = input_signal.X[0]
            x_end = input_signal.X[-1]
        else:
            if input_signal.X[0] < x_start:
                x_start = input_signal.X[0]
            if input_signal.X[-1] > x_end:
                x_end = input_signal.X[-1]
    padded_signals = []
    for input_signal in system.input_signals:
        if not input_signal.X[0] == x_start or not input_signal.X[-1] == x_end:
            new_signal = Signal.TimeSignal(
                x_start=x_start,
                x_end=x_end,
                delta_x=input_signal.delta_x,
                bit_depth=input_signal.bit_depth,
                codomain=input_signal.codomain,
                channels=input_signal.channels,
                units=input_signal.units
            )
            start_index = new_signal.get_nearest_sample_index(input_signal.X[0])
            end_index = new_signal.get_nearest_sample_index(input_signal.X[-1])
            new_signal.Y[start_index:end_index, :] = input_signal.Y[:, :]
            padded_signals.append(new_signal)
        else:
            padded_signals.append(input_signal)

    # Forward propagation
    completed_connectors = [0] * len(system.connectors)
    for connector in system.connectors:
        pass








