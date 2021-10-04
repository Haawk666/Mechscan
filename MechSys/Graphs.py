# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals
from . import utils
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Vertex:

    def __init__(self, i):
        self.i = i
        self.out_neighbourhood = []


class Digraph:

    def __init__(self):
        self.vertices = []

    def order(self):
        return len(self.vertices)

    def size(self):
        size = 0
        for vertex in self.vertices:
            size += len(vertex.out_neighbourhood)
        return size

    def BFS(self, starting_vertices):
        que = utils.Queue()
        for vertex in starting_vertices:
            que.enqueue(vertex)

        while not len(que) == 0:

            yield que.que[0]



