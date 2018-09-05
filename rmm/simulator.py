# -*- coding: utf-8 -*-
# simulator.py
# author: Antoine Passemiers

from rmm.utils import SCREEN_RESOLUTION

import numpy as np
    

class Simulator:

    def __init__(self, mouse):
        self.mouse = mouse
    
    def simulate(self):
        while True:
            x, y = self.random_coords()
            self.mouse.move_to(x, y)

    def random_coords(self):
        x = np.random.randint(0, SCREEN_RESOLUTION[0])
        y = np.random.randint(0, SCREEN_RESOLUTION[1])
        return x, y
