# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party

# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class System:

    def __init__(self):
        self.input_signals = []
        self.output_signals = []
        self.system_type = 'generic'
        self.path = None

    def add_input_signal(self, signal):
        self.input_signals.append(signal)

    def add_output_signal(self, signal):
        self.output_signals.append(signal)

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def info(self):
        return ''

    def save(self, path_string):
        pass

    def load(self, path_string):
        pass

    @staticmethod
    def static_load(path_string):
        pass


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

    def info(self):
        return ''

    def simulate(self):
        pass

    def save(self, path_string):
        pass

    def load(self, path_string):
        pass

    @staticmethod
    def static_load(path_string):
        pass




