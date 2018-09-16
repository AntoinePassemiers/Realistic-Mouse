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
    
    def sample(self):
        threshold = random.random()
        is_lower = np.diff((threshold < self.proba).astype(np.int))
        sample = np.where(is_lower == 1)[0][0]
        return sample
