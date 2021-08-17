# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party

# Internals
import Signals as ss
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemLTI:

    def __init__(self):

        self.input_signals = []
        self.output_signals = []

        self.path = None

    def __str__(self):
        return 'LTI system'

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def simulate(self):
        pass

    def save(self, path_string):
        pass

    def load(self, path_string):
        pass

    @staticmethod
    def static_load(path_string):
        pass




