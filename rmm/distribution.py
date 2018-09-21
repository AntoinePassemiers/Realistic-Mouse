# -*- coding: utf-8 -*-
# distribution.py
# author: Antoine Passemiers

from rmm.utils import CLICK_FILE_PATH

import random
import numpy as np


class Distribution:

    def __init__(self, pdf):
        self.pdf = np.asarray(pdf)
        self.pdf = self.pdf / pdf.sum()
        self.proba = np.cumsum(self.pdf)
        self.proba[:50] = 0.
        self.proba[-1] = 1.
    
    def sample(self, n_samples=1):
        threshold = random.random()
        is_lower = np.diff((threshold <= self.proba).astype(np.int))
        samples = np.where(is_lower == 1)[0]
        return samples[0]


if __name__ == '__main__':

    pdf = np.load(CLICK_FILE_PATH)
    d = Distribution(pdf)

    samples = [d.sample() for i in range(1000)]

    import matplotlib.pyplot as plt
    plt.switch_backend('TKAgg')
    plt.hist(samples)
    plt.show()
