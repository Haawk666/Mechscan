# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Queue:

    def __init__(self):
        self.que = []
        self.processed = []

    def __len__(self):
        return len(self.que)

    def enqueue(self, i):
        if i not in self.que and i not in self.processed:
            self.que.append(i)

    def dequeue(self):
        self.processed.append(self.que.pop(0))
        return self.processed[-1]



