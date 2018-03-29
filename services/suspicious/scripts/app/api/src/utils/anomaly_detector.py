import numpy as np
from numpy import histogram
from scipy.stats import chisquare


class AnomalyDetector:
    def __init__(self, h=5, alpha=0.7):
        self.h = h
        self.alpha = alpha
        self.memmory = []
        self.p = 0

    def estimate(self, number):
        self.memmory.append(number)
        self.memmory = self.memmory[-self.h:]

        if len(self.memmory) < self.h:
            a = 1
            self.p = (1 - self.alpha / a) * self.p + self.alpha / a * self.count_p()
        else:
            self.p = (1 - self.alpha) * self.p + self.alpha * self.count_p()
        return self.p

    def count_p(self):
        bins = 10
        hbatch = np.array(histogram(self.memmory, bins=bins))
        test = chisquare(hbatch[0])
        return 1 - test.pvalue


class AnomalyDetectorManager:
    def __init__(self, d=1, h=10, alpha=0.5):
        self.detectors = [AnomalyDetector(h=h, alpha=alpha) for i in range(d)]
        self.w = 1.0 / d

    def estimate(self, characteristics):
        proba = 0
        for k, v in enumerate(characteristics):
            proba += self.detectors[k].estimate(v) / self.w

        return proba