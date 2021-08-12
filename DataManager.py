# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
import numpy as np
import h5py
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TimeSignal:

    def __init__(self, t_start=0.0, t_end=10.0, sampling_rate=44000.0):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        self.f_a = sampling_rate  # Sampling rate
        self.t_start = t_start  # Timestamp signal start
        self.t_end = t_end  # Timestamp signal end

        self.T = 1 / self.f_a  # Sampling interval
        self.omega_a = 2 * np.pi / self.T  # Angular sampling frequency
        self.n = int(((self.t_end - self.t_start) / self.T) - 1.0)  # Number of samples

        self.X = np.linspace(self.t_start, self.t_end, num=self.n)  # Discrete time
        self.Y = np.zeros((self.n, ), dtype=float)  # Signal amplitude

    def __str__(self):
        info_string = 'Time signal:\n--------------------\n'
        info_string += 'Start time: {}\n'.format(self.t_start)
        info_string += 'End time: {}\n'.format(self.t_end)
        info_string += 'Sampling rate: {}\n'.format(self.f_a)
        info_string += 'Sampling interval: {}\n'.format(self.T)
        info_string += 'Angular sampling frequency: {}\n'.format(self.omega_a)
        info_string += 'Number of samples: {}\n'.format(self.n)
        info_string += 'X shape: {}\n'.format(self.X.shape)
        info_string += 'Y shape: {}\n'.format(self.Y.shape)
        return info_string

    def generate(self, function):
        """Generate signal from **function** which must be vectorized"""
        self.Y = function(self.X)

    def save(self):
        print(self)

    def load(self, path_string):
        # h5py.get_config().track_order = True
        #
        # with h5py.File(path_string, 'w') as f:
        #
        #     f.create_dataset('X', data=self.X)
        #
        #
        #     f.attrs['subtitle'] = self.subtitle
        #     f.attrs['speaker'] = self.speaker
        #     f.attrs['speaker_address'] = self.speaker_address
        #     f.attrs['date'] = self.date
        #     f.attrs['event'] = self.event
        #     f.attrs['use_parts'] = self.use_parts
        #
        #     f.create_group('structure/parts')
        #     for part in self.parts:
        #         f.create_group('structure/parts/{}'.format(part.title))
        #         for section in part.sections:
        #             f.create_group('structure/parts/{}/{}'.format(part.title, section.title))
        #             for subsection in section.subsections:
        #                 f.create_group('structure/parts/{}/{}/{}'.format(part.title, section.title, subsection))
        #
        #     f.create_group('structure/sections')
        #     for section in self.sections:
        #         f.create_group('structure/sections/{}'.format(section.title))
        #         for subsection in section.subsections:
        #             f.create_group('structure/sections/{}/{}'.format(section.title, subsection))
        #
        #     f.create_group('logos')
        #     for i, logo in enumerate(self.logos):
        #         print(logo['fname'])
        #         f['logos'].attrs['logo {}'.format(i)] = logo['fname']
        #
        #     f.create_group('colors/col_background')
        #     f['colors/col_background'].attrs['r'] = self.col_background[0]
        #     f['colors/col_background'].attrs['g'] = self.col_background[1]
        #     f['colors/col_background'].attrs['b'] = self.col_background[2]
        #     f.create_group('colors/col_highlight')
        #     f['colors/col_highlight'].attrs['r'] = self.col_highlight[0]
        #     f['colors/col_highlight'].attrs['g'] = self.col_highlight[1]
        #     f['colors/col_highlight'].attrs['b'] = self.col_highlight[2]
        #     f.create_group('colors/col_tertiary')
        #     f['colors/col_tertiary'].attrs['r'] = self.col_tertiary[0]
        #     f['colors/col_tertiary'].attrs['g'] = self.col_tertiary[1]
        #     f['colors/col_tertiary'].attrs['b'] = self.col_tertiary[2]
        pass

