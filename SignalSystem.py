# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
# 3rd party
import numpy as np
import wave
import h5py
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TimeSignal:

    def __init__(self, t_start=0.0, t_end=10.0, sampling_rate=44100.0, bit_depth=16):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        self.f_a = sampling_rate  # Sampling rate (Hz)
        self.bit_depth = bit_depth  # Bits (bits / sample)
        self.bit_rate = self.f_a * self.bit_depth  # Bitrate (bits / s)
        self.t_start = t_start  # Timestamp signal start (s)
        self.t_end = t_end  # Timestamp signal end (s)

        self.T = 1 / self.f_a  # Sampling interval (s)
        self.omega_a = 2 * np.pi / self.T  # Angular sampling frequency (Hz)
        self.n = int(((self.t_end - self.t_start) / self.T) - 1.0)  # Number of samples (#)

        self.X = np.linspace(self.t_start, self.t_end, num=self.n)  # Discrete time (s)
        self.Y = np.zeros((self.n, ), dtype=eval('np.int{}'.format(bit_depth)))  # Signal amplitude ()

    def __str__(self):
        info_string = 'Time signal:\n--------------------\n'
        info_string += 'Start time: {}\n'.format(self.t_start)
        info_string += 'End time: {}\n'.format(self.t_end)
        info_string += 'Sampling rate: {}\n'.format(self.f_a)
        info_string += 'Bit depth: {}\n'.format(self.bit_depth)
        info_string += 'Bitrate: {}\n'.format(self.bit_rate)
        info_string += 'Sampling interval: {}\n'.format(self.T)
        info_string += 'Angular sampling frequency: {}\n'.format(self.omega_a)
        info_string += 'Number of samples: {}\n'.format(self.n)
        info_string += 'X shape: {}\n'.format(self.X.shape)
        info_string += 'Y shape: {}\n'.format(self.Y.shape)
        return info_string

    def check(self, fix=False):
        """Check that all attributes are correct and makes sense. If fix=True, will try to fix problems (might be
        very buggy). Returns True if all attributes are coherent, false if not."""
        print('(t_start + T * (n + 1) | t_end) = ({} | {})'.format(self.t_start + self.T * (self.n + 1), self.t_end))
        print('(n | X.shape[0]) = ({} | {})'.format(self.n, self.X.shape[0]))
        print('(Y.dtype | bit depth) = {} | {})'.format(self.Y.dtype, self.bit_depth))
        print('(8 * Y.dtype.itemsize | bit depth) = ({} | {})'.format(8 * self.Y.dtype.itemsize, self.bit_depth))

    def generate(self, function):
        """Generate signal from **function** which must be vectorized"""
        self.Y = function(self.X)

    def add_noise_gauss(self, mu, sigma):
        for k, y in enumerate(self.Y):
            self.Y[k] += random.gauss(mu, sigma)

    def save(self, path_string):

        print(self)

        with h5py.File(path_string, 'w') as f:

            f.create_dataset('X', data=self.X)
            f.create_dataset('Y', data=self.Y)

            f.attrs['f_a'] = self.f_a
            f.attrs['bit_depth'] = self.bit_depth
            f.attrs['bit_rate'] = self.bit_rate
            f.attrs['t_start'] = self.t_start
            f.attrs['t_end'] = self.t_end
            f.attrs['T'] = self.T
            f.attrs['omega_a'] = self.omega_a
            f.attrs['n'] = self.n

    def load(self, path_string):

        with h5py.File(path_string, 'r') as f:

            self.X = f['X'][()]
            self.Y = f['Y'][()]

            self.f_a = f.attrs['f_a']
            self.bit_depth = f.attrs['bit_depth']
            self.bit_rate = f.attrs['bit_rate']
            self.t_start = f.attrs['t_start']
            self.t_end = f.attrs['t_end']
            self.T = f.attrs['T']
            self.omega_a = f.attrs['omega_a']
            self.n = f.attrs['n']

    @staticmethod
    def from_data(X, Y):
        if not X.shape == Y.shape:
            raise ValueError

        t_start = X[0]
        t_end = X[-1]
        n = X.shape[0]
        T = (t_end - t_start) / (n + 1.0)
        f_a = 1 / T
        bit_depth = 8 * Y.dtype.itemsize
        new_signal = TimeSignal(t_start=t_start, t_end=t_end, sampling_rate=f_a, bit_depth=bit_depth)
        new_signal.Y = Y

        return new_signal

    @staticmethod
    def from_wav(file_path):
        wav = wave.open(file_path, mode='rb')
        f_a = wav.getframerate()
        T = 1 / f_a
        n = wav.getnframes()
        t_end = T * (n + 1)
        nchan = wav.getnchannels()
        bitsize = 8 * wav.getsampwidth()
        dstr = wav.readframes(n * nchan)
        data = np.fromstring(dstr, eval('np.int{}'.format(bitsize)))
        data = np.reshape(data, (-1, nchan))
        result = TimeSignal(t_start=0.0, t_end=t_end, sampling_rate=f_a, bit_depth=bitsize)
        if nchan > 1:
            result.Y = data[:, 0] // 2 + data[:, 1] // 2
        else:
            result.Y = data[:, 0]
        return result

    def export_wav_signal(self, file_path):
        wav = wave.open(file_path, mode='wb')
        wav.setnchannels(1)
        wav.setsampwidth(self.bit_depth // 8)
        wav.setframerate(self.f_a)
        wav.setnframes(self.n)
        wav.writeframes(self.Y.astype('<h').tobytes())

