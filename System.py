# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import copy
import pathlib
# 3rd party
import h5py
# Internals
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class System:

    def __init__(self):
        self.path = None
        self.type = 'generic'
        self.system_axis = []
        self.components = []
        self.connectors = []

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def get_input_components(self, get_index=True):
        input_components = []
        for c, component in enumerate(self.components):
            if component.type == 'input':
                if get_index:
                    input_components.append((c, component))
                else:
                    input_components.append(component)
        return input_components

    def get_output_components(self, get_index=True):
        output_components = []
        for c, component in enumerate(self.components):
            if component.type == 'output':
                if get_index:
                    output_components.append((c, component))
                else:
                    output_components.append(component)
        return output_components

    def pad_signals(self):
        x_start = None
        x_end = None
        delta_x = None
        bit_depth = None
        codomain = None
        channels = None
        units = None
        for s, input_signal in enumerate([input_component[1].signal for input_component in self.get_input_components()]):
            if s == 0:
                x_start = input_signal.X[0]
                x_end = input_signal.X[-1]
                delta_x = input_signal.delta_x
                bit_depth = input_signal.bit_depth
                codomain = input_signal.codomain
                channels = input_signal.channels
                units = input_signal.units
            else:
                if input_signal.X[0] < x_start:
                    x_start = input_signal.X[0]
                if input_signal.X[-1] > x_end:
                    x_end = input_signal.X[-1]

        for i, input_component in enumerate([input_component for input_component in self.get_input_components()]):
            if not input_component[1].signal.X[0] == x_start or not input_component[1].signal.X[-1] == x_end:
                new_signal = Signal.TimeSignal(
                    x_start=x_start,
                    x_end=x_end,
                    delta_x=delta_x,
                    bit_depth=bit_depth,
                    codomain=codomain,
                    channels=channels,
                    units=units
                )
                start_index = new_signal.get_nearest_sample_index(input_component[1].signal.X[0])
                end_index = new_signal.get_nearest_sample_index(input_component[1].signal.X[-1])
                new_signal.Y[start_index:end_index, :] = input_component[1].signal.Y[:, :]
                self.components[input_component[0]].signal = new_signal
        for output_component in self.get_output_components():
            new_signal = Signal.TimeSignal(
                x_start=x_start,
                x_end=x_end,
                delta_x=delta_x,
                bit_depth=bit_depth,
                codomain=codomain,
                channels=channels,
                units=units
            )
            self.components[output_component[0]].signal = copy.deepcopy(new_signal)
        self.system_axis = copy.deepcopy(self.get_input_components(get_index=False)[0].signal.X)
        return self.system_axis

    def add_system(self, system):
        self.components.append(SysSystem(system))

    def add_input(self, signal):
        self.components.append(SysInput(signal))

    def add_output(self):
        self.components.append(SysOutput())

    def add_add(self):
        self.components.append(SysAdd())

    def add_split(self):
        self.components.append(SysSplit())

    def add_sum(self):
        self.components.append(SysSum())

    def add_delay(self):
        self.components.append(SysDelay())

    def add_scale(self, coefficient):
        self.components.append(SysScale(coefficient))

    def add_connector(self, connector):
        self.connectors.append(connector)

    def save(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:

            f.attrs['system_type'] = self.type
            f.create_dataset('system_axis', data=self.system_axis)
            f.attrs['num_components'] = len(self.components)
            f.attrs['num_connectors'] = len(self.connectors)

            for c, component in enumerate(self.components):
                f.attrs['component_{}'.format(c)] = component.type
                if component.type == 'input':
                    f.attrs['component_{}_path'.format(c)] = str(component.signal.path)
                elif component.type == 'scale':
                    f.attrs['component_{}_coefficient'.format(c)] = component.coefficient
                elif component.type == 'system':
                    f.attrs['component_{}_path'.format(c)] = str(component.system.path)

            for c, connector in enumerate(self.connectors):
                f.attrs['connector_{}_a'.format(c)] = connector[0][0]
                f.attrs['connector_{}_i'.format(c)] = connector[0][1]
                f.attrs['connector_{}_b'.format(c)] = connector[1][0]
                f.attrs['connector_{}_j'.format(c)] = connector[1][1]

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.type = 'generic'
            self.system_axis = f['system_axis'][()]
            self.components = []
            self.connectors = []

            num_components = int(f.attrs['num_components'])
            num_connectors = int(f.attrs['num_connectors'])

            for c in range(num_components):
                component_type = f.attrs['component_{}'.format(c)]
                if component_type == 'input':
                    signal = Signal.TimeSignal.static_load(f.attrs['component_{}_path'.format(c)])
                    self.add_input(signal)
                elif component_type == 'system':
                    system = System.static_load(f.attrs['component_{}_path'.format(c)])
                    self.add_system(system)
                elif component_type == 'scale':
                    coefficient = float(f.attrs['component_{}_coefficient'.format(c)])
                    self.add_scale(coefficient)
                elif component_type == 'add':
                    self.add_add()
                elif component_type == 'split':
                    self.add_split()
                elif component_type == 'output':
                    self.add_output()
                elif component_type == 'sum':
                    self.add_sum()
                elif component_type == 'delay':
                    self.add_delay()
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


class Node:

    def __init__(self):
        self.value = 0


class SysSystem:

    def __init__(self, system):

        self.system = system
        self.in_nodes = []
        self.out_nodes = []
        self.type = 'system'
        for input_component in self.system.get_input_components():
            c = input_component[0]
            self.system.components[c].signal = None
            self.in_nodes.append(Node())
        for output_component in self.system.get_output_components():
            c = output_component[0]
            self.system.components[c].signal = None
            self.out_nodes.append(Node())

    def transfer(self):

        for i, input_component in enumerate(self.system.get_input_components()):
            c = input_component[0]
            self.system.components[c].out_nodes[0].value = self.in_nodes[i].value
        for c, connector in enumerate(self.system.connectors):
            ((a, i), (b, j)) = connector
            self.system.components[b].in_nodes[j].value = self.system.components[a].out_nodes[i].value
        for c, component in enumerate(self.system.components):
            if component.type == 'output':
                pass
            elif component.type == 'input':
                pass
            else:
                component.transfer()
        for i, output_component in enumerate(self.system.get_output_components()):
            c = output_component[0]
            self.out_nodes[i].value = self.system.components[c].in_nodes[0].value


class SysInput:

    def __init__(self, signal):

        self.signal = signal
        self.in_nodes = []
        self.out_nodes = [Node()]
        self.type = 'input'

    def transfer(self, k):
        self.out_nodes[0].value = self.signal.Y[k, 0]


class SysOutput:

    def __init__(self):
        self.signal = None
        self.in_nodes = [Node()]
        self.out_nodes = []
        self.type = 'output'

    def transfer(self, k):
        self.signal.Y[k, 0] = self.in_nodes[0].value


class SysAdd:

    def __init__(self):
        self.in_nodes = [Node(), Node()]
        self.out_nodes = [Node()]
        self.type = 'add'

    def transfer(self):
        self.out_nodes[0].value = self.in_nodes[0].value + self.in_nodes[1].value


class SysSplit:

    def __init__(self):
        self.in_nodes = [Node()]
        self.out_nodes = [Node(), Node()]
        self.type = 'split'

    def transfer(self):
        self.out_nodes[0].value = self.in_nodes[0].value
        self.out_nodes[1].value = self.in_nodes[0].value


class SysSum:

    def __init__(self):
        self.in_nodes = [Node()]
        self.out_nodes = [Node()]
        self.type = 'sum'
        self.memory = 0

    def transfer(self):
        self.out_nodes[0].value = self.in_nodes[0].value + self.memory
        self.memory = self.out_nodes[0].value


class SysDelay:

    def __init__(self):
        self.in_nodes = [Node()]
        self.out_nodes = [Node()]
        self.type = 'delay'
        self.memory = 0

    def transfer(self):
        self.out_nodes[0].value = self.memory
        self.memory = self.in_nodes[0].value


class SysScale:

    def __init__(self, coefficient):
        self.in_nodes = [Node()]
        self.out_nodes = [Node()]
        self.type = 'scale'
        self.coefficient = coefficient

    def transfer(self):
        self.out_nodes[0].value = self.coefficient * self.in_nodes[0].value

