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

    def add_out_neighbour(self, j):
        if j not in self.out_neighbourhood:
            self.out_neighbourhood.append(j)


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

    def out_degree(self, i):
        return len(self.vertices[i].out_neighbourhood)

    def in_degree(self, i):
        in_degree = 0
        for vertex in self.vertices:
            if i in vertex.out_neighbourhood:
                in_degree += 1
        return in_degree

    def BFS(self, starting_vertices):
        que = utils.Queue()
        for vertex in starting_vertices:
            que.enqueue(vertex)

        while not len(que) == 0:

            for out_neighbour in self.vertices[que.que[0]].out_neighbourhood:
                que.enqueue(out_neighbour)
            yield que.que[0]
            que.dequeue()



