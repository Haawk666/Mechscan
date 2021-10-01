# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import copy
import pathlib
# 3rd party
import numpy as np
import h5py
# Internals
import Signal
import System_processing
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ComponentSystem:

    def __init__(self, system):
        self.system = system
        self.in_nodes = []
        self.out_nodes = []
        self.type = 'system'
        for component in self.system.components:
            if component.type == 'input':
                self.in_nodes.append(Node())
            if component.type == 'output':
                self.out_nodes.append(Node())

    def transfer(self):
        k = 0
        for c, component in enumerate(self.system.components):
            if component.type == 'input':
                self.system.components[c].signal = self.in_nodes[k].signal
                k += 1
        out_signals = System_processing.simulate(self.system)
        for i, signal in enumerate(out_signals):
            self.out_nodes[i].signal = signal


class ComponentSplitter:

    def __init__(self):

        self.in_nodes = [Node()]
        self.out_nodes = [Node(), Node()]
        self.type = 'splitter'

    def transfer(self):
        signal_1 = self.in_nodes[0].signal
        signal_2 = copy.deepcopy(signal_1)
        signal_3 = copy.deepcopy(signal_1)
        self.out_nodes[0].signal = signal_2
        self.out_nodes[1].signal = signal_3


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

    def add_system(self, system):
        self.components.append(ComponentSystem(system))

    def add_input_signal(self, signal):
        self.components.append(ComponentInput(signal))

    def add_output_signal(self):
        self.components.append(ComponentOutput())

    def add_adder(self):
        self.components.append(ComponentAdder())

    def add_splitter(self):
        self.components.append(ComponentSplitter())

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

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:

            f.attrs['system_type'] = self.system_type

            f.attrs['num_components'] = len(self.components)
            f.attrs['num_connectors'] = len(self.connectors)

            for c, component in enumerate(self.components):
                f.attrs['component_{}'.format(c)] = component.type

                if component.type == 'input':

                    f.create_dataset('component_{}_X'.format(c), data=component.signal.X)
                    f.attrs['component_{}_f_s'.format(c)] = component.signal.f_s
                    f.attrs['component_{}_delta_x'.format(c)] = component.signal.delta_x
                    f.attrs['component_{}_n'.format(c)] = component.signal.n
                    f.create_dataset('component_{}_Y'.format(c), data=component.signal.Y)

                    f.attrs['component_{}_type_id'.format(c)] = component.signal.type_id
                    f.attrs['component_{}_codomain'.format(c)] = component.signal.codomain
                    f.attrs['component_{}_channels'.format(c)] = component.signal.channels
                    f.attrs['component_{}_dimensions'.format(c)] = component.signal.dimensions
                    f.attrs['component_{}_bit_depth'.format(c)] = component.signal.bit_depth
                    f.attrs['component_{}_signal_type'.format(c)] = component.signal.signal_type
                    f.attrs['component_{}_N'.format(c)] = component.signal.N
                    f.attrs['component_{}_x_unit'.format(c)] = component.signal.units[0]
                    f.attrs['component_{}_y_unit'.format(c)] = component.signal.units[1]
                    f.attrs['component_{}_path'.format(c)] = str(component.signal.path)

            for c, connector in enumerate(self.connectors):
                f.attrs['connector_{}_a'.format(c)] = connector[0][0]
                f.attrs['connector_{}_i'.format(c)] = connector[0][1]
                f.attrs['connector_{}_b'.format(c)] = connector[1][0]
                f.attrs['connector_{}_j'.format(c)] = connector[1][1]

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.components = []
            self.connectors = []
            self.system_type = 'generic'

            num_components = int(f.attrs['num_components'])
            num_connectors = int(f.attrs['num_connectors'])

            for c in range(num_components):
                component_type = f.attrs['component_{}'.format(c)]
                if component_type == 'input':
                    signal = Signal.TimeSignal()
                    signal.type_id = int(f.attrs['component_{}_type_id'.format(c)])
                    signal.codomain = f.attrs['component_{}_codomain'.format(c)]
                    signal.channels = int(f.attrs['component_{}_channels'.format(c)])
                    signal.dimensions = int(f.attrs['component_{}_dimensions'.format(c)])
                    signal.bit_depth = int(f.attrs['component_{}_bit_depth'.format(c)])
                    signal.signal_type = str(f.attrs['component_{}_signal_type'.format(c)])
                    signal.N = int(f.attrs['component_{}_N'.format(c)])
                    signal.units = [f.attrs['component_{}_x_unit'.format(c)], f.attrs['component_{}_y_unit'.format(c)]]
                    signal.X = f['component_{}_X'.format(c)][()]
                    signal.f_s = f.attrs['component_{}_f_s'.format(c)]
                    signal.delta_x = float(f.attrs['component_{}_delta_x'.format(c)])
                    signal.x_start = signal.X[0]
                    signal.x_end = signal.X[-1]
                    signal.n = int(f.attrs['component_{}_n'.format(c)])
                    signal.Y = f['component_{}_Y'.format(c)][()]
                    signal.path = pathlib.Path(f.attrs['component_{}_path'.format(c)])
                    self.add_input_signal(signal)
                elif component_type == 'adder':
                    self.add_adder()
                elif component_type == 'splitter':
                    self.add_splitter()
                elif component_type == 'output':
                    self.add_output_signal()
                else:
                    raise TypeError('Unknown signal type')

            for c in range(num_connectors):
                a = f.attrs['connector_{}_a'.format(c)]
                i = f.attrs['connector_{}_i'.format(c)]
                b = f.attrs['connector_{}_b'.format(c)]
                j = f.attrs['connector_{}_j'.format(c)]
                self.add_connector(((a, i), (b, j)))

    @staticmethod
    def static_load(path_string):
        system = System()
        system.load(path_string=path_string)
        return system

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


