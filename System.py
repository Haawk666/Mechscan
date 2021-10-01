# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
import numpy as np
# Internals
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ComponentAdder:

    def __init__(self):

        self.in_nodes = [Node(), Node()]
        self.out_nodes = [Node()]
        self.type = 'adder'

    def transfer(self):
        signal_1 = self.in_nodes[0].signal
        signal_2 = self.in_nodes[1].signal
        signal_3 = Signal.TimeSignal(
            x_start=signal_1.x_start,
            x_end=signal_1.x_end,
            delta_x=signal_1.delta_x,
            bit_depth=signal_1.bit_depth,
            codomain=signal_1.codomain,
            channels=signal_1.channels,
            units=signal_1.units
        )
        signal_3.Y = np.add(signal_1.Y, signal_2.Y)
        self.out_nodes[0].signal = signal_3


class ComponentOutput:

    def __init__(self):
        self.out_nodes = []
        self.in_nodes = [Node()]
        self.type = 'output'

    def transfer(self):
        pass


class ComponentInput:

    def __init__(self, signal):
        self.signal = signal
        self.out_nodes = [Node()]
        self.in_nodes = []
        self.type = 'input'

    def transfer(self):
        self.out_nodes[0].signal = self.signal


class Node:

    def __init__(self, signal=None):
        self.signal = signal


class System:

    def __init__(self):
        self.components = []
        self.connectors = []
        self.system_type = 'generic'
        self.path = None

    def add_input_signal(self, signal):
        self.components.append(ComponentInput(signal=signal))

    def add_output_signal(self):
        self.components.append(ComponentOutput())

    def add_adder(self):
        self.components.append(ComponentAdder())

    def add_connector(self, connector):
        self.connectors.append(connector)

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def info(self):
        return ''

    def save(self, path_string):
        pass

    def load(self, path_string):
        pass

    @staticmethod
    def static_load(path_string):
        pass

    def input_signals(self):
        signals = []
        for component in self.components:
            if component.type == 'input':
                signals.append(component.signal)
        return signals

    def pad_signals(self):
        x_start = None
        x_end = None
        for s, input_signal in enumerate(self.input_signals()):
            if s == 0:
                x_start = input_signal.X[0]
                x_end = input_signal.X[-1]
            else:
                if input_signal.X[0] < x_start:
                    x_start = input_signal.X[0]
                if input_signal.X[-1] > x_end:
                    x_end = input_signal.X[-1]
        for c, component in enumerate(self.components):
            if component.type == 'input':
                if not component.signal.X[0] == x_start or not component.signal.X[-1] == x_end:
                    new_signal = Signal.TimeSignal(
                        x_start=x_start,
                        x_end=x_end,
                        delta_x=component.signal.delta_x,
                        bit_depth=component.signal.bit_depth,
                        codomain=component.signal.codomain,
                        channels=component.signal.channels,
                        units=component.signal.units
                    )
                    start_index = new_signal.get_nearest_sample_index(component.signal.X[0])
                    end_index = new_signal.get_nearest_sample_index(component.signal.X[-1])
                    new_signal.Y[start_index:end_index, :] = component.signal.Y[:, :]
                    self.components[c].signal = new_signal


class SystemLTI:

    def __init__(self):

        self.input_signals = []
        self.output_signals = []

        self.path = None

    def __str__(self):
        return 'LTI system'

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def info(self):
        return ''

    def simulate(self):
        pass

    def save(self, path_string):
        pass

    def load(self, path_string):
        pass

    @staticmethod
    def static_load(path_string):
        pass


