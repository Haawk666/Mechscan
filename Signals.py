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

    def __init__(self, x_start=0.0, x_end=10.0, delta_x=1.0/44100.0, bit_depth=16, codomain='int', channels=1):

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

        self.n = int(np.round(((self.x_end - self.x_start) / self.delta_x) - 1.0, decimals=0))
        self.X = np.linspace(self.x_start, self.x_end, num=self.n, dtype=np.float64)
        self.N = self.n

        self.channels = channels
        self.bit_depth = bit_depth

        self.Y = np.zeros((self.n, self.channels), dtype=eval(self.valid_types[self.type_id]))

        self.path = None
        self.signal_type = 'generic_1D'

    def __str__(self):
        info_str_1, info_str_2 = self.info()
        return info_str_1 + info_str_2

    def info(self):
        info_str_1 = 'dimensions: \t{}\n'.format(self.dimensions)
        info_str_1 += 'x_start: \t{}\n'.format(self.x_start)
        info_str_1 += 'x_end: \t{}\n'.format(self.x_end)
        info_str_1 += 'f_s: \t{}\n'.format(self.f_s)
        info_str_1 += 'delta_x: \t{}\n'.format(self.delta_x)
        info_str_1 += 'n: \t{}\n'.format(self.n)
        info_str_1 += 'N: \t{}\n'.format(self.N)

        info_str_2 = 'type: \t{}\n'.format(self.valid_types[self.type_id])
        info_str_2 += 'type id: \t{}\n'.format(self.type_id)
        info_str_2 += 'bit depth: \t{}\n'.format(self.bit_depth)
        info_str_2 += 'channels: \t{}\n'.format(self.channels)
        info_str_2 += 'Y.shape: \t{}\n'.format(self.Y.shape)

        return info_str_1, info_str_2

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

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

    def __init__(self, x_start=None, x_end=None, delta_x=None, bit_depth=16, codomain='int', channels=1):

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
            self.x_start = [0.0]
            self.x_end = [10.0]
            self.delta_x = [1.0 / 44100.0]
            self.dimensions = 1
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
            self.n.append(int(np.round(((end - start) / delta) - 1.0, decimals=0)))
            self.X.append(np.linspace(start, end, num=self.n[-1], dtype=np.float64))
        self.N = sum(self.n)

        self.channels = channels
        self.bit_depth = bit_depth

        self.Y = np.zeros(tuple(self.n + [self.channels]), dtype=eval(self.valid_types[self.type_id]))

        self.path = None
        self.signal_type = 'generic_nD'

    def __str__(self):
        info_str_1, info_str_2 = self.info()
        return info_str_1 + info_str_2

    def info(self):
        info_str_1 = 'dimensions: \t{}\n'.format(self.dimensions)
        info_str_1 += 'x_start: \t{}\n'.format(self.x_start)
        info_str_1 += 'x_end: \t{}\n'.format(self.x_end)
        info_str_1 += 'f_s: \t{}\n'.format(self.f_s)
        info_str_1 += 'delta_x: \t{}\n'.format(self.delta_x)
        info_str_1 += 'n: \t{}\n'.format(self.n)
        info_str_1 += 'N: \t{}\n'.format(self.N)

        info_str_2 = 'type: \t{}\n'.format(self.valid_types[self.type_id])
        info_str_2 += 'type id: \t{}\n'.format(self.type_id)
        info_str_2 += 'bit depth: \t{}\n'.format(self.bit_depth)
        info_str_2 += 'channels: \t{}\n'.format(self.channels)
        info_str_2 += 'Y.shape: \t{}\n'.format(self.Y.shape)

        return info_str_1, info_str_2

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


class TimeSignal(Signal):

    def __init__(self, x_start=0.0, x_end=10.0, delta_x=1.0/44100.0, bit_depth=16, codomain='int', channels=1):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        super().__init__(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
        self.signal_type = 'time'

    def check(self, fix=False):
        """Check that all attributes are correct and makes sense. If fix=True, will try to fix problems (might be
        very buggy). Returns True if all attributes are coherent, false if not."""
        print('(t_start + T * (n + 1) | t_end) = ({} | {})'.format(self.x_start + self.delta_x * (self.n + 1), self.x_end))
        print('(n | X.shape[0]) = ({} | {})'.format(self.n, self.X.shape[0]))
        print('(Y.dtype | bit depth) = {} | {})'.format(self.Y.dtype, self.bit_depth))
        print('(8 * Y.dtype.itemsize | bit depth) = ({} | {})'.format(8 * self.Y.dtype.itemsize, self.bit_depth))

    def generate(self, function):
        for k, x in enumerate(self.X):
            self.Y[k, 0] = function(x)

    def generate_spectrum(self, function):
        pass

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
        delta_x = (x_end - x_start) / (n + 1.0)
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        channels = Y.shape[-1]
        new_signal = TimeSignal(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
        new_signal.Y = Y

        return new_signal

    @staticmethod
    def from_frequency(frequency_signal):
        f_s = 2 * frequency_signal.X[-1]
        delta_x = 1 / f_s
        if frequency_signal.time_signal is not None:
            x_start = frequency_signal.time_signal.X[0]
        else:
            x_start = 0.0
        x_end = delta_x * (2 * frequency_signal.n + 1) + x_start
        Y = np.fft.ifft(np.concatenate((frequency_signal.Y, frequency_signal.Y[1::, :].flip()), axis=0), axis=0)
        time_signal = TimeSignal(x_start=x_start, x_end=x_end, delta_x=delta_x)

    @staticmethod
    def from_wav(file_path):
        """Does not yet support 24 bit wav."""
        wav = wave.open(file_path, mode='rb')
        f_s = wav.getframerate()
        delta_x = 1.0 / f_s
        n = wav.getnframes()
        t_end = delta_x * (n + 1)
        nchan = wav.getnchannels()
        bitsize = 8 * wav.getsampwidth()
        dstr = wav.readframes(n * nchan)
        data = np.fromstring(dstr, eval('np.int{}'.format(bitsize)))
        data = np.reshape(data, (-1, nchan))
        result = TimeSignal(x_start=0.0, x_end=t_end, delta_x=delta_x, bit_depth=bitsize, codomain='int', channels=nchan)
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

    def __init__(self, x_start=0.0, x_end=22050.0, delta_x=0.1, bit_depth=128, codomain='complex', channels=1):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        super().__init__(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
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
        delta_x = (x_end - x_start) / (n + 1.0)
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        channels = Y.shape[-1]
        new_signal = FrequencySignal(x_start=x_start, x_end=x_end, delta_x=delta_x, bit_depth=bit_depth, codomain=codomain, channels=channels)
        new_signal.Y = Y

        return new_signal

    @staticmethod
    def from_time_signal(time_signal):
        Y_f = np.fft.fft(time_signal.Y, axis=0)[:time_signal.n // 2]
        X_f = np.fft.fftfreq(n=time_signal.n, d=1 / time_signal.f_s)[:time_signal.n // 2]
        frequency_signal = FrequencySignal.from_data(X_f, Y_f)
        frequency_signal.time_signal = time_signal
        return frequency_signal




