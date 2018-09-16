# -*- coding: utf-8 -*-
# click.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse
from rmm.move import *
from rmm.utils import *

import msvcrt
import numpy as np
import scipy.interpolate


if __name__ == '__main__':

    if not os.path.isfile('click_diffs.npy'):
        hist = np.zeros(500, dtype=np.int)
    else:
        hist = np.load('click_diffs.npy')

    last_click = None
    c = b'e'
    while c != b'q':
        c = msvcrt.getch()
        if c == b' ':
            click = MouseMovement.time_millis()
            if last_click is not None:
                if click - last_click < 500.0:
                    hist[int(click - last_click)] += 1
        last_click = click


    import matplotlib.pyplot as plt
    plt.switch_backend('TKAgg')
    plt.plot(hist)
    plt.show()

    np.save('click_diffs.npy', hist)