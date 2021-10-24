# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party

# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def replace_nan(data, strategy='mean'):

    if strategy == 'mean':

        for i in range(len(data.frame)):
            for c, column in enumerate(data.frame):
                if str(data.frame.values[i, c]) == 'nan':
                    print('{} | {}'.format(data.frame.values[i, c], 'True'))

    return data
