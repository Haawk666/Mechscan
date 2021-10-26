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

        for c, column in enumerate(data.frame):
            data.frame[column] = data.frame[column].fillna(data.frame[column].mean())
            if update is not None:
                update.setValue(c)

    return data





