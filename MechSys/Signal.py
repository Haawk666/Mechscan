# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import pathlib
from abc import ABC
# 3rd party
import numpy as np
import wave
import h5py
# import sounddevice
import librosa
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Signal(ABC):

    valid_types = [
        'np.int8',
        'np.int16',
        'np.int32',
        'np.int64',
        'np.complex64',
        'np.complex128',
        'np.float16',
        'np.float32',
        'np.float64',
        'np.bool_'
    ]

    def __init__(self, x_start=0.0, x_end=10.0, delta_x=1.0/44100.0, bit_depth=16, codomain='int', channels=1, units=None):

        if units is None:
            self.units = ['1', '1']
        else:
            self.units = units

        if 'np.{}{}'.format(codomain, bit_depth) in self.valid_types:
            self.type_id = self.valid_types.index('np.{}{}'.format(codomain, bit_depth))
        elif codomain == 'bool':
            self.type_id = self.valid_types.index('np.bool_')
        else:
            self.type_id = -1
            logger.info('type error')
            print('type error')
            raise TypeError

        self.x_start = x_start
        self.x_end = x_end
        self.delta_x = delta_x
        self.dimensions = 1

        self.f_s = 1.0 / self.delta_x

        self.n = int(np.round(((self.x_end - self.x_start) / self.delta_x) + 1.0, decimals=0))
        self.X = np.linspace(self.x_start, self.x_end, num=self.n, dtype=np.float64)
        self.N = self.n

        self.channels = channels
        self.bit_depth = bit_depth

        self.Y = np.zeros((self.n, self.channels), dtype=eval(self.valid_types[self.type_id]))

        self.codomain = self.Y.dtype.name.replace('{}'.format(self.bit_depth), '')

        self.path = None
        self.signal_type = 'generic_1D'

    def __str__(self):
        meta_data = self.info()
        info_string = ''
        for key, value in meta_data.items():
            info_string += '{}: {}\n'.format(key, value)
        return info_string

    def info(self):

        meta_data = {
            'x_start': self.x_start,
            'x_end': self.x_end,
            'delta_x': self.delta_x,
            'f_s': self.f_s,
            'n': self.n,
            'bit_depth': self.bit_depth,
            'codomain': self.codomain,
            '': '',
            'N': self.N,
            'signal_type': self.signal_type,
            'type_id': self.type_id,
            'type': self.valid_types[self.type_id],
            'channels': self.channels,
            'dimensions': self.dimensions,
            'x units': self.units[0],
            'y units': self.units[1],
            'Y.shape': self.Y.shape,
            'Y.dtype': self.Y.dtype,
            'X.shape': self.X.shape,
            'X.dtype': self.X.dtype
        }

        return meta_data

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def length(self):
        return self.x_end - self.x_start

    def save(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:

            f.create_dataset('X', data=self.X)
            f.attrs['f_s'] = self.f_s
            f.attrs['delta_x'] = self.delta_x
            f.attrs['x_start'] = self.x_start
            f.attrs['x_end'] = self.x_end
            f.attrs['n'] = self.n
            f.create_dataset('Y', data=self.Y)

            f.attrs['type_id'] = self.type_id
            f.attrs['codomain'] = self.codomain
            f.attrs['channels'] = self.channels
            f.attrs['dimensions'] = self.dimensions
            f.attrs['bit_depth'] = self.bit_depth
            f.attrs['signal_type'] = self.signal_type
            f.attrs['N'] = self.N
            f.attrs['x_unit'] = self.units[0]
            f.attrs['y_unit'] = self.units[1]

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.type_id = int(f.attrs['type_id'])
            self.codomain = f.attrs['codomain']
            self.channels = int(f.attrs['channels'])
            self.dimensions = int(f.attrs['dimensions'])
            self.bit_depth = int(f.attrs['bit_depth'])
            self.signal_type = str(f.attrs['signal_type'])
            self.N = int(f.attrs['N'])
            self.units = [f.attrs['x_unit'], f.attrs['y_unit']]

            self.X = f['X'][()]
            self.f_s = f.attrs['f_s']
            self.delta_x = float(f.attrs['delta_x'])
            self.x_start = self.X[0]
            self.x_end = self.X[-1]
            self.n = int(f.attrs['n'])

            self.Y = f['Y'][()]

    @staticmethod
    def static_load(path_string):
        signal = Signal()
        signal.load(path_string)
        return signal

    def play(self, channel=1):

        sounddevice.play(self.Y[:, channel - 1], self.f_s)

    def get_nearest_sample_index(self, x):
        residual = np.absolute(x - self.X[0])
        residual_index = 0
        for k, t in enumerate(self.X):
            if np.absolute(x - t) < residual:
                residual = np.absolute(x - t)
                residual_index = k
        return residual_index


class MultiSignal(ABC):

    valid_types = [
        'np.int8',
        'np.int16',
        'np.int32',
        'np.int64',
        'np.complex64',
        'np.complex128',
        'np.float16',
        'np.float32',
        'np.float64',
        'np.bool_'
    ]

    def __init__(self, x_start=None, x_end=None, delta_x=None, bit_depth=128, codomain='complex', channels=1, units=None):

        if units is None:
            self.units = ['s', '1']
        else:
            self.units = units

        if 'np.{}{}'.format(codomain, bit_depth) in self.valid_types:
            self.type_id = self.valid_types.index('np.{}{}'.format(codomain, bit_depth))
        elif codomain == 'bool':
            self.type_id = self.valid_types.index('np.bool_')
        else:
            self.type_id = -1
            logger.info('type error')
            print('type error')
            raise TypeError

        if x_start is None and x_end is None and delta_x is None:
            self.x_start = [0.0, 0.0]
            self.x_end = [10.0, 44100.0 / 2]
            self.delta_x = [1.0 / 44100.0, 1.0]
            self.dimensions = 2
        elif x_start is not None and x_end is not None and delta_x is not None:
            if len(x_start) == len(x_end) and len(x_start) == len(delta_x):
                self.x_start = x_start
                self.x_end = x_end
                self.delta_x = delta_x
                self.dimensions = len(self.x_start)
            else:
                self.x_start = x_start
                self.x_end = x_end
                self.delta_x = delta_x
                self.dimensions = len(self.x_start)
                logger.info('input error')
                print('input error')
                raise TypeError
        else:
            self.x_start = x_start
            self.x_end = x_end
            self.delta_x = delta_x
            self.dimensions = len(self.x_start)
            logger.info('input error')
            print('input error')
            raise TypeError

        self.f_s = []
        for dim_delta_x in self.delta_x:
            self.f_s.append(1.0 / dim_delta_x)

        self.n = []
        self.X = []
        for start, end, delta in zip(self.x_start, self.x_end, self.delta_x):
            self.n.append(int(np.round(((end - start) / delta) + 1.0, decimals=0)))
            self.X.append(np.linspace(start, end, num=self.n[-1], dtype=np.float64))
        self.N = 1
        for n in self.n:
            self.N *= n

        self.channels = channels
        self.bit_depth = bit_depth

        self.Y = np.zeros(tuple(self.n + [self.channels]), dtype=eval(self.valid_types[self.type_id]))

        self.codomain = self.Y.dtype.name.replace('{}'.format(self.bit_depth), '')

        self.path = None
        self.signal_type = 'generic_nD'

    def __str__(self):
        meta_data = self.info()
        info_string = ''
        for key, value in meta_data.items():
            info_string += '{}: {}\n'.format(key, value)
        return info_string

    def info(self):

        meta_data = {
            'x_start': self.x_start,
            'x_end': self.x_end,
            'delta_x': self.delta_x,
            'f_s': self.f_s,
            'n': self.n,
            'bit_depth': self.bit_depth,
            'codomain': self.codomain,
            '': '',
            'N': self.N,
            'signal_type': self.signal_type,
            'type_id': self.type_id,
            'type': self.valid_types[self.type_id],
            'channels': self.channels,
            'dimensions': self.dimensions,
            'x units': self.units[0],
            'y units': self.units[1],
            'Y.shape': self.Y.shape,
            'Y.dtype': self.Y.dtype,
        }

        for i in range(self.dimensions):
            meta_data['X[{}].shape'.format(i)] = self.X[i].shape

        return meta_data

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def save(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:
            for i, X in enumerate(self.X):
                f.create_dataset('X_{}'.format(i), data=X)
                f.attrs['f_s_{}'.format(i)] = self.f_s[i]
                f.attrs['delta_x_{}'.format(i)] = self.delta_x[i]
                f.attrs['x_start_{}'.format(i)] = self.x_start[i]
                f.attrs['x_end_{}'.format(i)] = self.x_end[i]
                f.attrs['n_{}'.format(i)] = self.n[i]
            f.create_dataset('Y', data=self.Y)

            f.attrs['type_id'] = self.type_id
            f.attrs['channels'] = self.channels
            f.attrs['dimensions'] = self.dimensions
            f.attrs['bit_depth'] = self.bit_depth
            f.attrs['signal_type'] = self.signal_type
            f.attrs['N'] = self.N

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.type_id = int(f.attrs['type_id'])
            self.channels = int(f.attrs['channels'])
            self.dimensions = int(f.attrs['dimensions'])
            self.bit_depth = int(f.attrs['bit_depth'])
            self.signal_type = str(f.attrs['signal_type'])
            self.N = int(f.attrs['N'])

            self.X = []
            self.f_s = []
            self.delta_x = []
            self.x_start = []
            self.x_end = []
            self.n = []
            for i in range(self.dimensions):
                self.X.append(f['X_{}'.format(i)][()])
                self.f_s.append(float(f.attrs['f_s_{}'.format(i)]))
                self.delta_x.append(float(f.attrs['delta_x_{}'.format(i)]))
                self.x_start.append(self.X[-1][0])
                self.x_end.append(self.X[-1][-1])
                self.n.append(self.X[-1].shape[0])

            self.Y = f['Y'][()]

    @staticmethod
    def static_load(path_string):
        signal = Signal()
        signal.load(path_string)
        return signal

    def play(self, channel=1):

        sounddevice.play(self.Y[:, 0, channel - 1], self.f_s[0])

    def get_nearest_sample_index(self, x, axis=0):
        residual = np.absolute(x - self.X[axis][0])
        residual_index = 0
        for k, t in enumerate(self.X[axis]):
            if np.absolute(x - t) < residual:
                residual = np.absolute(x - t)
                residual_index = k
        return residual_index


class TimeSignal(Signal):

    def __init__(self, x_start=0.0, x_end=10.0, delta_x=1.0/44100.0, bit_depth=16, codomain='int', channels=1, units=None):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        if units is None:
            units = ['s', '1']
        super().__init__(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels, units=units)
        self.signal_type = 'time'

    @staticmethod
    def static_load(path_string):
        time_signal = TimeSignal()
        time_signal.load(path_string)
        return time_signal

    @staticmethod
    def from_data(X, Y):
        if not X.shape[0] == Y.shape[0]:
            raise ValueError

        x_start = X[0]
        x_end = X[-1]
        n = X.shape[0]
        delta_x = X[1] - X[0]
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        channels = Y.shape[-1]
        new_signal = TimeSignal(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
        new_signal.Y = Y

        return new_signal

    @staticmethod
    def from_wav(file_path):
        """Does not yet support 24 bit wav."""
        wav = wave.open(file_path, mode='rb')
        f_s = np.float64(wav.getframerate())
        delta_x = np.float64(1.0) / f_s
        n = wav.getnframes()
        t_end = delta_x * (n - 1)
        nchan = wav.getnchannels()
        bitsize = 8 * wav.getsampwidth()
        dstr = wav.readframes(n * nchan)
        data = np.fromstring(dstr, eval('np.int{}'.format(bitsize)))
        data = np.reshape(data, (-1, nchan))
        result = TimeSignal(x_start=0.0, x_end=t_end, delta_x=delta_x, bit_depth=bitsize, codomain='int', channels=nchan)
        result.Y = data
        return result

    @staticmethod
    def from_mp3(file_path):
        data, f_s = librosa.load(file_path, sr=None, mono=False, dtype=np.float64)
        if data.shape[0] == 2:
            channels = 2
            data = np.reshape(data, (-1, channels))
        else:
            channels = 1
            data = np.reshape(data, (-1, 1))

        delta_x = np.float64(1.0) / f_s
        t_end = delta_x * (data.shape[0] - 1)

        result = TimeSignal(x_start=0.0, x_end=t_end, delta_x=delta_x, bit_depth=64, codomain='float', channels=channels)
        result.Y = data
        return result

    def export_wav_signal(self, file_path):
        wav = wave.open(file_path, mode='wb')
        wav.setnchannels(self.channels)
        wav.setsampwidth(self.bit_depth // 8)
        wav.setframerate(self.f_s)
        wav.setnframes(self.n)
        wav.writeframes(self.Y.astype('<h').tobytes())


class FrequencySignal(Signal):

    def __init__(self, x_start=-22050.0, x_end=22050.0, delta_x=0.1, bit_depth=128, codomain='complex', channels=1, units=None):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        if units is None:
            units = ['Hz', '1']
        super().__init__(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels, units=units)
        self.time_signal = None
        self.signal_type = 'frequency'

    def generate(self, real_function, im_function):
        for k, x in enumerate(self.X):
            self.Y[k][0] = real_function(x)
            self.Y[k][1] = im_function(x)

    @staticmethod
    def from_data(X, Y):
        if not X.shape[0] == Y.shape[0]:
            raise ValueError

        x_start = X[0]
        x_end = X[-1]
        n = X.shape[0]
        delta_x = (x_end - x_start) / (n - 1.0)
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        channels = Y.shape[-1]
        new_signal = FrequencySignal(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
        new_signal.Y = Y

        return new_signal


class TimeFrequencySignal(MultiSignal):

    def __init__(self, x_start=None, x_end=None, delta_x=None, bit_depth=128, codomain='complex', channels=1, units=None):
        if units is None:
            units = ['s', 'Hz', '1']
        super().__init__(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels, units=units)
        self.time_signal = None
        self.signal_type = 'time-frequency'

    def generate(self, function):
        pass

    @staticmethod
    def from_data(X, Y):
        shape_x = [X[0].shape[0], X[1].shape[0]]
        shape_y = [Y.shape[0], Y.shape[1]]
        if not shape_y == shape_x:
            raise ValueError

        x_start = [X[0][0], X[1][0]]
        x_end = [X[0][-1], X[1][-1]]
        n = [X[0].shape[0], X[1].shape[0]]
        delta_x = [(x_end[0] - x_start[0]) / (n[0] - 1.0), (x_end[1] - x_start[1]) / (n[1] - 1.0)]
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        channels = Y.shape[-1]

        time_frequency_signal = TimeFrequencySignal(
            x_start=x_start,
            x_end=x_end,
            delta_x=delta_x,
            bit_depth=bit_depth,
            codomain=codomain,
            channels=channels
        )

        time_frequency_signal.Y = Y

        return time_frequency_signal



