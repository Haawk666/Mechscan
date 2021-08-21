# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import pathlib
# 3rd party
import numpy as np
import wave
import h5py
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Signal:

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

        self.x_start = x_start
        self.x_end = x_end
        self.delta_x = delta_x
        self.f_x = 1.0 / self.delta_x
        self.channels = channels
        self.bit_depth = bit_depth
        self.bit_rate = self.channels * self.f_x * self.bit_depth
        self.n = int(np.round(((self.x_end - self.x_start) / self.delta_x) - 1.0, decimals=0))

        self.X = np.linspace(self.x_start, self.x_end, num=self.n, dtype=np.float64)
        self.Y = np.zeros((self.n, self.channels), dtype=eval(self.valid_types[self.type_id]))

        self.path = None
        self.signal_type = 'generic'

    def __str__(self):
        info_str_1, info_str_2 = self.info()
        return info_str_1 + info_str_2

    def info(self):
        info_str_1 = 'x_start: \t{}\n'.format(self.x_start)
        info_str_1 += 'x_end: \t{}\n'.format(self.x_end)
        info_str_1 += 'f_x: \t{}\n'.format(self.f_x)
        info_str_1 += 'delta_x: \t{}\n'.format(self.delta_x)
        info_str_1 += 'n: \t{}\n'.format(self.n)

        info_str_2 = 'type: \t{}\n'.format(self.valid_types[self.type_id])
        info_str_2 += 'bit depth: \t{}\n'.format(self.bit_depth)
        info_str_2 += 'bit rate: \t{}\n'.format(self.bit_rate)
        info_str_2 += 'channels: \t{}\n'.format(self.channels)

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
            f.create_dataset('Y', data=self.Y)

            f.attrs['type_id'] = self.type_id
            f.attrs['channels'] = self.channels
            f.attrs['f_x'] = self.f_x
            f.attrs['bit_depth'] = self.bit_depth
            f.attrs['bit_rate'] = self.bit_rate
            f.attrs['x_start'] = self.x_start
            f.attrs['x_end'] = self.x_end
            f.attrs['delta_x'] = self.delta_x
            f.attrs['n'] = self.n

    def load(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'r') as f:

            self.X = f['X'][()]
            self.Y = f['Y'][()]

            self.type_id = int(f.attrs['type_id'])
            self.channels = int(f.attrs['channels'])
            self.f_x = float(f.attrs['f_x'])
            self.bit_depth = int(f.attrs['bit_depth'])
            self.bit_rate = float(f.attrs['bit_rate'])
            self.x_start = np.float64(f.attrs['x_start'])
            self.x_end = np.float64(f.attrs['x_end'])
            self.delta_x = float(f.attrs['delta_x'])
            self.n = int(f.attrs['n'])

    @staticmethod
    def static_load(path_string):
        signal = Signal()
        signal.load(path_string)
        return signal


class TimeSignal:

    def __init__(self, *args):
        """Init a signal with a given **sampling rate** and start and end timestamps."""
        super.__init__(*args)
        self.signal_type = 'time'

    def check(self, fix=False):
        """Check that all attributes are correct and makes sense. If fix=True, will try to fix problems (might be
        very buggy). Returns True if all attributes are coherent, false if not."""
        print('(t_start + T * (n + 1) | t_end) = ({} | {})'.format(self.t_start + self.delta_t * (self.n + 1), self.t_end))
        print('(n | X.shape[0]) = ({} | {})'.format(self.n, self.X.shape[0]))
        print('(Y.dtype | bit depth) = {} | {})'.format(self.Y.dtype, self.bit_depth))
        print('(8 * Y.dtype.itemsize | bit depth) = ({} | {})'.format(8 * self.Y.dtype.itemsize, self.bit_depth))

    def generate(self, function):
        for k, x in enumerate(self.X):
            self.Y[k] = function(x)

    def generate_spectrum(self, function):
        pass

    def save(self, path_string):

        self.path = pathlib.Path(path_string)

        with h5py.File(path_string, 'w') as f:

            f.create_dataset('X', data=self.X)
            f.create_dataset('Y', data=self.Y)

            f.attrs['f_a'] = self.f_a
            f.attrs['bit_depth'] = self.bit_depth
            f.attrs['bit_rate'] = self.bit_rate
            f.attrs['t_start'] = self.t_start
            f.attrs['t_end'] = self.t_end
            f.attrs['T'] = self.delta_t
            f.attrs['omega_a'] = self.omega_a
            f.attrs['n'] = self.n

    @staticmethod
    def static_load(path_string):
        signal = TimeSignal()
        signal.load(path_string)
        return signal

    @staticmethod
    def from_data(X, Y):
        if not X.shape[0] == Y.shape[0]:
            raise ValueError

        t_start = X[0]
        t_end = X[-1]
        n = X.shape[0]
        T = (t_end - t_start) / (n + 1.0)
        f_a = 1 / T
        bit_depth = 8 * Y.dtype.itemsize
        codomain = Y.dtype.name.replace(str(bit_depth), '')
        new_signal = TimeSignal(t_start=t_start, t_end=t_end, sampling_rate=f_a, bit_depth=bit_depth, codomain=codomain)
        new_signal.Y = Y

        return new_signal

    @staticmethod
    def from_wav(file_path):
        """Does not yet support 24 bit wav."""
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
        result = TimeSignal(t_start=0.0, t_end=t_end, sampling_rate=f_a, bit_depth=bitsize, codomain='int', channels=nchan)
        result.Y = data
        return result

    def export_wav_signal(self, file_path):
        wav = wave.open(file_path, mode='wb')
        wav.setnchannels(1)
        wav.setsampwidth(self.bit_depth // 8)
        wav.setframerate(self.f_a)
        wav.setnframes(self.n)
        wav.writeframes(self.Y.astype('<h').tobytes())


class FrequencySignal:

    def __init__(self, time_signal):

        self.old_X = time_signal.X
        self.Y_complex = np.fft.fftn(time_signal.Y)[:time_signal.n // 2]
        self.X = np.fft.fftfreq(n=time_signal.n, d=1 / time_signal.f_a)[:time_signal.n // 2]
        self.Y = np.absolute(self.Y_complex)

        self.f_start = self.X[0]
        self.f_end = self.X[-1]
        self.n = self.X.shape[0]
        self.delta_f = (self.f_end - self.f_start) / (self.n + 1.0)
        self.f_a = 1 / self.delta_f
        self.bit_depth = 8 * self.Y.dtype.itemsize
        self.codomain = self.Y.dtype.name.replace(str(self.bit_depth), '')
        self.channels = self.Y.shape[1]
        self.bit_rate = self.channels * self.f_a * self.bit_depth
        self.omega_a = 2 * np.pi / self.delta_f

        self.signal_type = 'frequency'

        self.path = None

    def __str__(self):
        return 'TODO'

    def info(self):
        info_string_1 = 'Start frequency: {}\n'.format(self.f_start)
        info_string_1 += 'End frequency: {}\n'.format(self.f_end)
        info_string_1 += 'Sampling rate: {}\n'.format(self.f_a)
        info_string_1 += 'Bit depth: {}\n'.format(self.bit_depth)
        info_string_1 += 'Bitrate: {}\n'.format(self.bit_rate)
        info_string_1 += 'Codomain type: {}\n'.format(self.codomain)
        info_string_1 += 'Signal type: {}\n'.format(self.signal_type)

        info_string_2 = 'Sampling interval: {}\n'.format(self.delta_f)
        info_string_2 += 'Angular sampling frequency: {}\n'.format(self.omega_a)
        info_string_2 += 'Number of samples: {}\n'.format(self.n)
        info_string_2 += 'Number of channels: {}\n'.format(self.channels)
        info_string_2 += 'X shape: {}\n'.format(self.X.shape)
        info_string_2 += 'Y shape: {}\n'.format(self.Y.shape)
        return info_string_1, info_string_2

    def name(self):
        if self.path is None:
            return 'New'
        else:
            return self.path.name

    def generate(self, real_function, im_function):
        for k, x in enumerate(self.X):
            self.Y[k][0] = real_function(x)
            self.Y[k][1] = im_function(x)

