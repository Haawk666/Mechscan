# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals
from . import Graph
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ANN:

    def __init__(self):
        self.graph = Graph.Digraph()
        self.path = None
        self.type = 'nn'

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def info(self):
        meta_data = {
            'Input nodes': self.get_property(property='inputs'),
            'Output nodes': self.get_property(property='outputs'),
            'Order': self.get_property(property='order'),
            'Size': self.get_property(property='size'),
        }

        return meta_data

    def get_property(self, property='order'):
        if property == 'order':
            return self.graph.order()
        elif property == 'size':
            return self.graph.size()
        elif property == 'inputs':
            inputs = 0
            for vertex in self.graph.vertices:
                if vertex.type == 'input':
                    inputs += 1
            return inputs
        elif property == 'outputs':
            outputs = 0
            for vertex in self.graph.vertices:
                if vertex.type == 'output':
                    outputs += 1
            return outputs
        elif property == 'layers':
            layers = 0
            for vertex in self.graph.vertices:
                if vertex.layer + 1 > layers:
                    layers = vertex.layer + 1
            return layers
        else:
            return None

    def add_input(self):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'input'
        vertex.activation = 0.0
        self.graph.vertices.append(vertex)

    def add_node(self, activation='sigmoid', layer=0):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'node'
        vertex.activation = 0.0
        vertex.layer = layer
        self.graph.vertices.append(vertex)

    def add_output(self):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'output'
        vertex.activation = 0.0
        self.graph.vertices.append(vertex)

    def connect(self, i, j):
        self.graph.vertices[i].add_out_neighbour(j)

    def fit(self, training_data):
        pass

    def evaluate(self, input_data):
        pass

    def accuracy(self, test_data):
        pass

    @staticmethod
    def from_params(params):
        ann = ANN()

        # Add nodes
        for i in range(params['inputs']):
            ann.add_input()
        for l in range(len(params['layers'])):
            nodes = params['layers'][l]['nodes']
            activation = params['layers'][l]['activation']
            for n in range(nodes):
                ann.add_node(activation=activation)
                if l == 0:
                    for vertex in ann.graph.vertices:
                        if vertex.type == 'input':
                            ann.connect(vertex.i, len(ann.graph.vertices) - 1)
                else:
                    for vertex in ann.graph.vertices:
                        if vertex.layer == l - 1:
                            ann.connect(vertex.i, len(ann.graph.vertices) - 1)
        for o in range(params['outputs']):
            ann.add_output()
            for vertex in ann.graph.vertices:
                if vertex.layer == ann.get_property(property='layers') - 1:
                    ann.connect(vertex.i, len(ann.graph.vertices) - 1)

        return ann



