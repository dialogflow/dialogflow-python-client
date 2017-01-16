# -*- coding: utf-8 -*-

import math
import numpy as np


class VAD(object):
    """docstring for VAD"""
    def __init__(self, sampleRate=16000):
        super(VAD, self).__init__()

        self.sampleRate = sampleRate

        self.reset()

    def reset(self):
        self.isFirst = True

        self.energyMAX = 0.0
        self.energyMIN = 0.0

        self.energyMIN_INITIAL = 0.1

        self.resetDelta()

        self.frameCount = 0
        self.inactiveFrameCount = 0
        self.activeFrameCount = 0

        self.threshold = 0

        self.lam = 0

        self.wait = True

    def resetDelta(self):
        self.delta = 1.01

    def energy(self, frame):
        result = 0.0

        for value in frame:
            result += value * value

        return math.sqrt(result / float(len(frame)))

    def processFrame(self, frame_input):
        state = 0

        frame = np.array(frame_input).astype(np.float32)
        frame = frame / float(np.iinfo(np.int16).max)

        energy = self.energy(frame)

        if self.isFirst:
            self.isFirst = False
            self.energyMAX = energy
            self.energyMIN_INITIAL = energy
            self.energyMIN = self.energyMIN_INITIAL
            return 1

        if energy > self.energyMAX:
            self.energyMAX = energy

        if energy < self.energyMIN:
            if energy < 0.025:
                self.energyMIN = self.energyMIN_INITIAL
            else:
                self.energyMIN = energy

            self.resetDelta()

        lam = abs(self.energyMAX - self.energyMIN) / (self.energyMAX + 0.01)

        threshold = (1. - lam) * self.energyMAX + lam * self.energyMIN
        self.threshold = threshold

        if energy * 1.01 > threshold and lam > 0.35:
            if self.activeFrameCount > 3:
                state = 1
                self.inactiveFrameCount = 0
                self.wait = False
            else:
                state = 0

            self.activeFrameCount += 1
        else:
            if self.inactiveFrameCount > 8 * 3:
                state = 0
                self.activeFrameCount = 0
            else:
                state = 1
                self.inactiveFrameCount += 1

        self.delta = self.delta * 1.001

        if state == 0 and self.wait:
            if self.inactiveFrameCount > 40:
                state = 0
                self.wait = False
            else:
                state = 1

        self.energyMIN = self.energyMIN * self.delta
        self.energyMAX = self.energyMAX * 0.999

        return state
