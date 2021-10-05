# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party

# Internals
from MechSys import Graphs
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

    # Set progress max
    if update is not None:
        update.setMaximum(system_axis.shape[0] - 1)

    # Ensure initial conditions
    for component in system.components:
        for node in component.in_nodes:
            node.value = 0
        for node in component.out_nodes:
            node.value = 0

    # Build graph
    graph = Graphs.Digraph()
    for c, component in enumerate(system.components):
        graph.vertices.append(Graphs.Vertex(c))
    for c, connector in enumerate(system.connectors):
        graph.vertices[connector[0][0]].out_neighbourhood.append(connector[1][0])

    # Simulate
    for k, x in enumerate(system_axis):

        # Set input nodes
        for input_component in system.get_input_components(get_index=False):
            input_component.transfer(k)

        # Transfer
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

        # Set progress
        if update is not None:
            update.setValue(k)

    # Prepare output
    result = []
    for output_component in system.get_output_components(get_index=False):
        result.append(output_component.signal)

    return result


def simulate_2(system, update=None):

    # Pad input signals
    system_axis = system.pad_signals()

    # Set progress max
    if update is not None:
        update.setMaximum(system_axis.shape[0] - 1)

    # Ensure initial conditions
    for component in system.components:
        for node in component.in_nodes:
            node.value = 0
        for node in component.out_nodes:
            node.value = 0

    # Build graph
    graph = Graphs.Digraph()
    for c, component in enumerate(system.components):
        graph.vertices.append(Graphs.Vertex(c))
    for c, connector in enumerate(system.connectors):
        graph.vertices[connector[0][0]].add_out_neighbour(connector[1][0])

    # Find input indices
    input_indices = []
    for input_component in system.get_input_components():
        input_indices.append(input_component[0])
    order = graph.BFS(input_indices)
    print([i for i in order])

    # Simulate
    for k, x in enumerate(system_axis):

        # Set input nodes
        for input_component in system.get_input_components(get_index=False):
            input_component.transfer(k)

        # Transfer
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

        # Set progress
        if update is not None:
            update.setValue(k)

    # Prepare output
    result = []
    for output_component in system.get_output_components(get_index=False):
        result.append(output_component.signal)

    return result



