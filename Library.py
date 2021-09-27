# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import numpy as np
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_settings_map():

    settings_map = {
        'GUI': {
            'Theme': {
                'type': 'string',
                'default': 'Dark',
                'options': ['Dark', 'Bright']
            },
            'Tooltips': {
                'type': 'bool',
                'default': True,
            },
            'Signal_interface': {
                'type': 'group',
                'members': {
                    'Display_signal_details': {
                        'type': 'string',
                        'default': 'All',
                        'options': ['All', 'Some', 'None']
                    }
                }
            }
        },
        'Plotting': {
            'Complex-valued_time_signals': {
                'type': 'group',
                'members': {
                    'Plot_real': {
                        'type': 'bool',
                        'default': True,
                    },
                    'Plot_imaginary': {
                        'type': 'bool',
                        'default': True
                    },
                    'Plot_magnitude': {
                        'type': 'bool',
                        'default': False
                    },
                    'Plot_phase': {
                        'type': 'bool',
                        'default': False
                    }
                }
            },
            'Complex-valued_frequency_signals': {
                'type': 'group',
                'members': {
                    'Y-axis': {
                        'type': 'string',
                        'default': 'Magnitude',
                        'options': ['Magnitude', 'Power', 'Decibel']
                    },
                    'Plot_phase': {
                        'type': 'bool',
                        'default': False
                    },
                    'Plot_negative_frequencies': {
                        'type': 'bool',
                        'default': False
                    }
                }
            }
        },
        'Systems': {
            'Sampling': {
                'type': 'string',
                'default': 'Interpolate',
                'options': ['Interpolate', 'Resample']
            }
        }
    }

    return settings_map


def get_default_settings_string():

    settings_map = get_settings_map()

    settings_string = ''

    for section, dict_ in settings_map.items():
        settings_string += '[{}]\n'.format(section)
        for key, value in dict_.items():
            if value['type'] == 'group':
                for member, dict__ in value['members'].items():
                    settings_string += '{} = {}\n'.format(key + '_' + member, str(dict__['default']))
            else:
                settings_string += '{} = {}\n'.format(key, str(value['default']))
        settings_string += '\n'

    return settings_string




