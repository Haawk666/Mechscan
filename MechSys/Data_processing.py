# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def replace_nan(data, strategy='mean', update=None):

    if strategy == 'mean':

        means = data.frame.mean()

        for i in range(len(data.frame)):
            for c, column in enumerate(data.frame):
                if data.frame.values[i, c] == 'nan':
                    data.frame.values[i, c] = means[c]
            if update is not None:
                update.setValue(i)

    return data





