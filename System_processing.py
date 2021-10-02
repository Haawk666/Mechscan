# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party

# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def calculate(system):

    # Pad input signals
    system.pad_signals()
    result = []
    return result


def simulate(system, update=None):

    # Pad input signals
    system_axis = system.pad_signals()

    if update is not None:
        update.setMaximum(system_axis.shape[0] - 1)

    for k, x in enumerate(system_axis):
        for input_component in system.get_input_components(get_index=False):
            input_component.transfer(k)
        for c, connector in enumerate(system.connectors):
            ((a, i), (b, j)) = connector
            system.components[b].in_nodes[j].value = system.components[a].out_nodes[i].value
        for c, component in enumerate(system.components):
            if component.type == 'output':
                component.transfer(k)
            elif component.type == 'input':
                pass
            else:
                component.transfer()
        if update is not None:
            update.setValue(k)

    result = []
    for output_component in system.get_output_components(get_index=False):
        result.append(output_component.signal)

    return result





