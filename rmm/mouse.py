# -*- coding: utf-8 -*-
# mouse.py
# author: Antoine Passemiers

from rmm.distribution import Distribution
from rmm.movement import MouseMovement
from rmm.shape import Shape, Box
from rmm.utils import *

import time
import random
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

        pdf = np.load(CLICK_FILE_PATH)
        self.click_distribution = Distribution(pdf)
    
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

    def linear_move(self, x, y):
        dt = .3 # TODO
        mouse_move_to_with_tweening(x, y, dt)

    def move_to(self, *args):
        print(args)
        if len(args) == 1 and isinstance(args[0], Shape):
            x1, y1 = args[0].sample()
        elif len(args) == 4:
            x1, y1 = Box(*args).sample()
            x1, y1 = self.random_coords_in_area(*args)
        else:
            x1, y1 = args[0], args[1]
        x0, y0 = self.get_position()
        _x0, _y0, _x1, _y1, movement = self.closest(x0, y0, x1, y1)
        assert((x0, y0) == (_x0, _y0))
        movement.replay()
        if len(args) == 4:
            if not ((args[0] <= _x1 <= args[2]) and \
                    (args[1] <= _y1 < args[3])):
                self.linear_move(x1, y1)
            else:
                if random.random() < 0.4: # TODO
                    self.linear_move(x1, y1)
        else:
            self.linear_move(x1, y1)
    
    def move_away_from(self, x0, y0, x1, y1):
        x, y = random.choice([(x0, y0), (x0, y1), (x1, y0), (x1, y1)])
        for i in range(5):
            _x = np.random.randint(0, SCREEN_RESOLUTION[0])
            _y = np.random.randint(0, SCREEN_RESOLUTION[1])
            if (x0 <= x < x1) and (y0 <= y < y1):
                x, y = _x, _y
                break
        # TODO: make (x, y) as close as possible to area
        self.move_to(self, x, y)

    def click(self, *args, **kwargs):
        self.left_click(*args, **kwargs)

    def left_click(self, n_clicks=1):
        for i in range(n_clicks):
            dt = self.click_distribution.sample() / 1000.0
            time.sleep(dt)
            mouse_left_click()
        # TODO: random move
    
    def right_click(self, n_clicks=1):
        for i in range(n_clicks):
            mouse_right_click()
            time.sleep(0.2)
        # TODO: random move

    def wait(self, n_seconds, p=0.5):
        if random.random() < p:
            time.sleep(n_seconds)
        else:
            time.sleep(n_seconds) # TODO: random moves
