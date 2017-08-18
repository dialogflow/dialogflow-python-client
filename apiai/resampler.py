# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
