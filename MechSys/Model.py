# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import pathlib
# 3rd party
import h5py
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
                if vertex.type == 'node':
                    if vertex.layer + 1 > layers:
                        layers = vertex.layer + 1
            return layers
        else:
            return None

    def get_arcs(self):
        arcs = []
        for vertex in self.graph.vertices:
            for j in vertex.out_neighbourhood:
                arcs.append((vertex.i, j))
        return arcs

    def get_layer_size(self, layer=0):
        if self.get_property(property='layers') - 1 > layer:
            size = 0
            for vertex in self.graph.vertices:
                if vertex.type == 'node':
                    if vertex.layer == layer:
                        size += 1
            return size
        else:
            return 0

    def get_layer_activation(self, layer=0):
        if self.get_property(property='layers') - 1 > layer:
            activation = ''
            for vertex in self.graph.vertices:
                if vertex.type == 'node':
                    if vertex.layer == layer:
                        activation = vertex.activation
            return activation
        else:
            return 0

    def get_params(self):
        params = dict()
        params['inputs'] = self.get_property(property='inputs')
        params['outputs'] = self.get_property(property='outputs')
        params['layers'] = []
        for l in range(self.get_property(property='layers')):
            params['layers'].append({
                'index': int(l),
                'activation': self.get_layer_activation(layer=l),
                'nodes': int(self.get_layer_size(layer=l))
            })
        return params

    def add_input(self, x=0.0, y=0.0, r=0.0):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'input'
        vertex.activation = 0.0
        vertex.x = x
        vertex.y = y
        vertex.r = r
        self.graph.vertices.append(vertex)

    def add_node(self, activation='sigmoid', layer=0, x=0.0, y=0.0, r=0.0):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'node'
        vertex.activation = 0.0
        vertex.layer = layer
        vertex.x = x
        vertex.y = y
        vertex.r = r
        self.graph.vertices.append(vertex)

    def add_output(self, x=0.0, y=0.0, r=0.0):
        vertex = Graph.Vertex(self.graph.order())
        vertex.type = 'output'
        vertex.activation = 0.0
        vertex.x = x
        vertex.y = y
        vertex.r = r
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

        x = 0
        y = 0

        # Add nodes
        for i in range(params['inputs']):
            ann.add_input(x=x, y=y)
            y += 30

        x = 30
        y = 0

        for l in range(len(params['layers'])):
            nodes = params['layers'][l]['nodes']
            activation = params['layers'][l]['activation']
            for n in range(nodes):
                ann.add_node(activation=activation, layer=l, x=x, y=y)
                y += 30
                if l == 0:
                    for vertex in ann.graph.vertices:
                        if vertex.type == 'input':
                            ann.connect(vertex.i, len(ann.graph.vertices) - 1)
                else:
                    for vertex in ann.graph.vertices:
                        if vertex.type == 'node':
                            if vertex.layer == l - 1:
                                ann.connect(vertex.i, len(ann.graph.vertices) - 1)
            x += 30
            y = 0

        for o in range(params['outputs']):
            ann.add_output(x=x, y=y)
            y += 30
            for vertex in ann.graph.vertices:
                if vertex.type == 'node':
                    if vertex.layer == ann.get_property(property='layers') - 1:
                        ann.connect(vertex.i, len(ann.graph.vertices) - 1)

        return ann

    def save(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:

            params = self.get_params()

            f.attrs['model_type'] = self.type

            f.attrs['inputs'] = params['inputs']
            f.attrs['outputs'] = params['outputs']
            f.attrs['depth'] = len(params['layers'])

            for l, layer in enumerate(params['layers']):
                f.attrs['layer_{}_index'.format(l)] = params['layers'][l]['index']
                f.attrs['layer_{}_activation'.format(l)] = params['layers'][l]['activation']
                f.attrs['layer_{}_nodes'.format(l)] = params['layers'][l]['nodes']

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.type = 'nn'

            params = dict()
            params['inputs'] = int(f.attrs['inputs'])
            params['outputs'] = int(f.attrs['outputs'])
            depth = int(f.attrs['depth'])
            params['layers'] = []
            for l in range(depth):
                params['layers'].append({
                    'index': int(f.attrs['layer_{}_index'.format(l)]),
                    'activation': f.attrs['layer_{}_activation'.format(l)],
                    'nodes': int(f.attrs['layer_{}_nodes'.format(l)])
                })

            self.graph = Graph.Digraph()

            x = 0
            y = 0

            # Add nodes
            for i in range(params['inputs']):
                self.add_input(x=x, y=y)
                y += 30

            x = 30
            y = 0

            for l in range(len(params['layers'])):
                nodes = params['layers'][l]['nodes']
                activation = params['layers'][l]['activation']
                for n in range(nodes):
                    self.add_node(activation=activation, layer=l, x=x, y=y)
                    y += 30
                    if l == 0:
                        for vertex in self.graph.vertices:
                            if vertex.type == 'input':
                                self.connect(vertex.i, len(self.graph.vertices) - 1)
                    else:
                        for vertex in self.graph.vertices:
                            if vertex.type == 'node':
                                if vertex.layer == l - 1:
                                    self.connect(vertex.i, len(self.graph.vertices) - 1)
                x += 30
                y = 0

            for o in range(params['outputs']):
                self.add_output(x=x, y=y)
                y += 30
                for vertex in self.graph.vertices:
                    if vertex.type == 'node':
                        if vertex.layer == self.get_property(property='layers') - 1:
                            self.connect(vertex.i, len(self.graph.vertices) - 1)

    @staticmethod
    def static_load(path_string):
        model = ANN()
        model.load(path_string=path_string)
        return model

