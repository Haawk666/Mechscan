# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import copy
# 3rd party

# Internals
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def simulate(system):

    # Pad input signals
    system.pad_signals()

    # Forward propagation
    completed_connectors = [1] * len(system.connectors)
    completed_components = [1] * len(system.components)
    simulating = True
    previous_sum = 0
    while simulating:
        for c, component in enumerate(system.components):
            if completed_components[c] == 1:
                in_complete = True
                for in_node in component.in_nodes:
                    if in_node.signal is None:
                        in_complete = False
                if in_complete:
                    system.components[c].transfer()
                    completed_components[c] = 0
        for c, connector in enumerate(system.connectors):
            if completed_connectors[c] == 1:
                ((a, i), (b, j)) = connector
                if system.components[a].out_nodes[i].signal is not None:
                    system.components[b].in_nodes[j].signal = copy.deepcopy(system.components[a].out_nodes[i].signal)
                    completed_connectors[c] = 0
        current_sum = sum(completed_connectors) + sum(completed_components)
        print(current_sum)
        if current_sum == 0:
            simulating = False
        if current_sum == previous_sum:
            simulating = False
        else:
            previous_sum = current_sum

    result = []
    for component in system.components:
        if component.type == 'output':
            result.append(component.in_nodes[0].signal)

    return result









