# -*- coding: utf-8 -*-
# mouse.py
# author: Antoine Passemiers

from rmm.movement import MouseMovement
from rmm.utils import *

import time
import copy
import numpy as np


class MouseMode:
    TRACKPAD = 'trackpad'
    MOUSE = 'mouse'


class RealisticMouse:

    def __init__(self, mode=MouseMode.TRACKPAD):
        movements = get_mv_data()
        self.mode = mode
        for mode in [MouseMode.TRACKPAD, MouseMode.MOUSE]:
            for i in range(len(movements[mode])):
                movements[mode][i] = MouseMovement.from_dict(movements[mode][i])
        self.movements = movements
        self.src = {
            MouseMode.TRACKPAD: np.asarray(
                [m.coords[0] for m in self.movements[MouseMode.TRACKPAD]]),
            MouseMode.MOUSE: np.asarray(
                [m.coords[0] for m in self.movements[MouseMode.MOUSE]])}
        self.dest = {
            MouseMode.TRACKPAD: np.asarray(
                [m.coords[-1] for m in self.movements[MouseMode.TRACKPAD]]),
            MouseMode.MOUSE: np.asarray(
                [m.coords[-1] for m in self.movements[MouseMode.MOUSE]])}

        if len(self.src[self.mode]) == 0:
            raise NoDataFoundException(
                'No data found for requested mode: "%s"' % self.mode)
    
    def closest(self, x0, y0, x1, y1):
        positions = np.concatenate(
            [self.src[self.mode], self.dest[self.mode]], axis=1)
        transformation = positions[:, :2] - np.asarray([x0, y0])
        positions[:, :2] -= transformation
        positions[:, 2:] -= transformation
        diff = np.sum(
            (positions - np.asarray([x0, y0, x1, y1])) ** 2, axis=1)
        c = np.argmin(diff)
        _x0, _y0, _x1, _y1 = positions[c]
        movement = self.movements[self.mode][c]
        movement = movement - transformation[c]
        return _x0, _y0, _x1, _y1, movement

    def get_position(self):
        return get_mouse_position()

    def ensure_position(self, x, y):
        assert(self.get_position() == (x, y))
    
    def unrealistic_move_to(self, x, y):
        dt = .3 # TODO
        mouse_move_to_with_tweening(x, y, dt)

    def random_coords_in_area(self, x1, y1, x2, y2):
        # Make sure that x2 > x1 and y2 > y1
        x = np.random.randint(x1, x2)
        y = np.random.randint(y1, y2)
        return x, y

    def move_to(self, *args):
        if len(args) == 4:
            x1, y1 = self.random_coords_in_area(*args)
        else:
            x1, y1 = args[0], args[1]
        x0, y0 = self.get_position()
        _x0, _y0, _x1, _y1, movement = self.closest(x0, y0, x1, y1)
        assert((x0, y0) == (_x0, _y0))
        movement.replay()
        self.unrealistic_move_to(x1, y1)
    
    def click(self, *args, **kwargs):
        self.left_click(*args, **kwargs)

    def left_click(self, n_clicks=1):
        for i in range(n_clicks):
            mouse_left_click()
            time.sleep(0.2)
        # TODO: random move
    
    def right_click(self, n_clicks=1):
        for i in range(n_clicks):
            mouse_right_click()
            time.sleep(0.2)
        # TODO: random move
