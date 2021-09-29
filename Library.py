# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import numpy as np
# Internals
import Functions as f
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


def get_function_map(signal):

    if signal.dimensions == 1:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = {
                'custom': {
                    'args': ['x'],
                    'kwargs': dict(),
                    'function': f.custom_R,
                    'vector': True
                },
                'sine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': f.sine_RR,
                    'vector': True
                },
                'cosine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': f.cosine_RR,
                    'vector': True
                },
                'pulse': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                    },
                    'function': f.gauss_RR,
                    'vector': True
                },
                'linear chirp': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'x_0': Parameter(signal.x_start, signal.x_end, 1.0, 2, signal.x_start),
                        'x_1': Parameter(signal.x_start, signal.x_end, 1.0, 2, signal.x_end),
                        'f_0': Parameter(0.0, 10000.0, 10.0, 1, 0.0),
                        'f_1': Parameter(0.0, 10000.0, 10.0, 1, 666.0)
                    },
                    'function': f.linear_chirp_RR,
                    'vector': True
                },
                'morlet wavelet': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0)
                    },
                    'function': f.morlet_wavelet_RR,
                    'vector': True
                }
            }

        else:

            functions = {
                'custom': {
                    'args': ['x'],
                    'kwargs': dict(),
                    'function': f.custom_R,
                    'vector': True
                },
                'sine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': f.sine_RC,
                    'vector': True
                },
                'cosine': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0),
                    },
                    'function': f.cosine_RC,
                    'vector': True
                },
                'complex morlet wavelet': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                        'f': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'phi': Parameter(-2 * np.pi, 2 * np.pi, 0.5 * np.pi, 3, 0.0)
                    },
                    'function': f.morlet_wavelet_RC,
                    'vector': True
                },
                'pulse': {
                    'args': ['x'],
                    'kwargs': {
                        'A': Parameter(-1000.0, 1000.0, 10.0, 1, 666.0),
                        'mu': Parameter(signal.X[0], signal.X[-1], 1.0, 3, (signal.X[-1] - signal.X[0]) / 2),
                        'sigma': Parameter(0.0, signal.X[-1] - signal.X[0], 1.0, 3, signal.X[-1] - signal.X[0]),
                    },
                    'function': f.gauss_RC,
                    'vector': True
                }
            }

    elif signal.dimensions == 2:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = {
                'custom': {
                    'args': ['x_1', 'x_2'],
                    'kwargs': dict(),
                    'function': f.custom_R2,
                    'vector': False
                }
            }

        else:

            functions = {
                'custom': {
                    'args': ['x_1', 'x_2'],
                    'kwargs': dict(),
                    'function': f.custom_R2,
                    'vector': False
                }
            }

    else:

        if signal.codomain in ['int', 'float', 'bool_']:

            functions = dict()

        else:

            functions = dict()

    return functions


class Parameter:

    def __init__(self, min, max, step, dec, default, value=None):

        self.min = min
        self.max = max
        self.step = step
        self.dec = dec
        self.default = default
        if value is None:
            self.value = self.default
        else:
            self.value = value


