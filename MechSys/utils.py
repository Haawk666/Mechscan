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

    def __len__(self):
        return len(self.que)

    def enqueue(self, i):
        if i not in self.que:
            self.que.append(i)

    def dequeue(self):
        return self.que.pop(0)



