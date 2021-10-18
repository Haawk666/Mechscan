# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import pathlib
# 3rd party
import pandas as pd
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Dataset:

    def __init__(self):
        self.dataframes = []
        self.path = None
        self.type = 'generic'

    def __str__(self):
        meta_data = self.info()
        info_string = ''
        for key, value in meta_data.items():
            info_string += '{}: {}\n'.format(key, value)
        return info_string

    def info(self):
        meta_data = {
            'Frames': len(self.dataframes),
            'Datapoints': sum([len(x) for x in self.dataframes])
        }

        return meta_data

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def import_csv(self, path_string):
        data = pd.read_csv(path_string)
        self.dataframes.append(data)




