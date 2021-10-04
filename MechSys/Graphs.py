# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals

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


