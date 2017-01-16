# -*- coding: utf-8 -*-

import numpy as np


class Resampler(object):
    def __init__(self,
                 source_samplerate,
                 destination_samplerate=16000,
                 dtype=np.int16,
                 channels=1):

        super(Resampler, self).__init__()
        self.ratio = destination_samplerate / float(source_samplerate)
        self.dtype = dtype
        self.channels = channels

    def resample(self, frame, frame_count):
        nparray = np.fromstring(frame, dtype=self.dtype)

        scale = self.ratio

        n = round(len(nparray) * scale)
        resampled = np.interp(
            np.linspace(0.0, 1.0, n, endpoint=False),
            np.linspace(0.0, 1.0, len(nparray), endpoint=False),
            nparray
        )

        return resampled.tolist(), resampled.astype(self.dtype).tostring()
