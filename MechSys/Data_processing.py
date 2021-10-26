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

        for c, column in enumerate(data):
            data[column] = data[column].fillna(data[column].mean())
            if update is not None:
                update.setValue(c)

    return data





