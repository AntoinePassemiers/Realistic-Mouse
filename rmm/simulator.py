# -*- coding: utf-8 -*-
# simulator.py
# author: Antoine Passemiers

from rmm.utils import *

import random
import numpy as np
    

class Simulator:

    def __init__(self, mouse):
        self.mouse = mouse
    
    def simulate(self):
        x0, y0 = get_mouse_position()
        while True:
            if random.random() > 0.15:
                x1, y1 = self.random_coords()
                if random.random() > 0.3:
                    print('Mouse movement: (%i, %i) -> (%i, %i)' % \
                        (x0, y0, x1, y1))
                    self.mouse.move_to(x1, y1)
                else:
                    print('Mouse move away from: (%i, %i, %i, %i)' % \
                        (x0, y0, x1, y1))
                    self.mouse.move_to(x1, y1)
                x0, y0 = x1, y1
            else:
                print('Click two times')
                self.mouse.click(n_clicks=2)

    def random_coords(self):
        x = np.random.randint(0, SCREEN_RESOLUTION[0])
        y = np.random.randint(0, SCREEN_RESOLUTION[1])
        return x, y
