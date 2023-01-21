# -*- coding: utf-8 -*-
# mouse.py
# author: Antoine Passemiers

import copy
import enum
import random
import time

import numpy as np

from rmm.distribution import Distribution
from rmm.movement import MouseMovement
from rmm.shape import Shape, Box, Point
from rmm.utils import *


class Mouse:

    class Mode(str, enum.Enum):

        TRACKPAD = 'trackpad'
        MOUSE = 'mouse'

    def __init__(
            self,
            n_closest_movements: int = 10,
            speed: float = 1.,
            mode: 'Mouse.Mode' = Mode.TRACKPAD,
            multi_monitor: bool = False
    ):
        self.n_closest_movements = n_closest_movements
        self.speed: float = speed
        self.backend = get_backend()
        movements = get_mv_data()
        self.multi_monitor = multi_monitor
        if multi_monitor:
            self.monitor_coords = get_monitor_coords()
        else:
            self.monitor_coords = None
        self.mode: Mouse.Mode = mode
        for mode in [Mouse.Mode.TRACKPAD, Mouse.Mode.MOUSE]:
            for i in range(len(movements[mode])):
                movements[mode][i] = MouseMovement.from_dict(movements[mode][i])
        self.movements = movements
        self.src = {
            Mouse.Mode.TRACKPAD: np.asarray(
                [m.coords[0] for m in self.movements[Mouse.Mode.TRACKPAD]]),
            Mouse.Mode.MOUSE: np.asarray(
                [m.coords[0] for m in self.movements[Mouse.Mode.MOUSE]])}
        self.dest = {
            Mouse.Mode.TRACKPAD: np.asarray(
                [m.coords[-1] for m in self.movements[Mouse.Mode.TRACKPAD]]),
            Mouse.Mode.MOUSE: np.asarray(
                [m.coords[-1] for m in self.movements[Mouse.Mode.MOUSE]])}

        if len(self.src[self.mode]) == 0:
            raise NoDataFoundException(
                'No data found for requested mode: "%s"' % self.mode)

        pdf = np.load(CLICK_FILE_PATH)
        self.click_distribution = Distribution(pdf)
    
    def __closest(self, x0: int, y0: int, x1: int, y1: int) -> Tuple[int, int, int, int, MouseMovement]:
        positions = np.concatenate(
            [self.src[self.mode], self.dest[self.mode]], axis=1)
        transformation = positions[:, :2] - np.asarray([x0, y0])
        positions[:, :2] -= transformation
        positions[:, 2:] -= transformation
        diff = np.sum(
            (positions - np.asarray([x0, y0, x1, y1])) ** 2, axis=1)
        if self.n_closest_movements == 1:
            c = np.argmin(diff)
        else:
            c = np.argsort(diff)[np.random.randint(1, self.n_closest_movements)]
        _x0, _y0, _x1, _y1 = positions[c]
        movement = self.movements[self.mode][c]
        movement = movement - transformation[c]
        return _x0, _y0, _x1, _y1, movement

    def get_position(self):
        return get_mouse_position()
    
    def convert_to_area(self, *args, monitor: int = 0):
        if len(args) == 1 and isinstance(args[0], Shape):
            area = copy.deepcopy(args[0])
        elif len(args) == 4:
            area = Box(*args)
        else:
            area = Point(*args)
        if self.multi_monitor and monitor > 0:
            dx = self.monitor_coords[monitor]['left']
            dy = self.monitor_coords[monitor]['top']
            area += (dx, dy)
        return area

    def move_to(self, *args, monitor: int = 0, n_moves: int = 2, full: bool = False):
        area = self.convert_to_area(*args, monitor=monitor)
        xf, yf = area.sample()
        x0, y0 = self.get_position()
        if (not area.contains(x0, y0)) or full:
            _x1, _y1 = x0, y0
            moves = list()
            for _ in range(n_moves):
                _, _, _x1, _y1, movement = self.__closest(_x1, _y1, xf, yf)
                moves.append(movement)
            _x2, _y2 = _x1, _y1
            for movement in moves:
                movement.replay(self.backend, speed=self.speed, multi_monitor=self.multi_monitor)
            if not isinstance(area, Point):
                if not area.contains(_x1, _y1):
                    MouseMovement.linear_tweening(
                        self.backend, xf, yf, multi_monitor=self.multi_monitor)
                else:
                    if random.random() < 0.4: # TODO
                        MouseMovement.linear_tweening(
                            self.backend, xf, yf, multi_monitor=self.multi_monitor)
            else:
                MouseMovement.linear_tweening(
                    self.backend, xf, yf, multi_monitor=self.multi_monitor)
    
    def move_away_from(self, x0: int, y0: int, x1: int, y1: int):
        # TODO: use convert_to_area
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
        x0, y0 = self.get_position()
        for x, y in [(x0-1, y0), (x0, y0), (x0+1, y0), (x0, y0)]:
            move_mouse_to(self.backend, x, y, multi_monitor=self.multi_monitor)
            time.sleep(0.05)
        self.left_click(*args, **kwargs)

    def left_click(self, n_clicks: int = 1):
        for i in range(n_clicks):
            dt = self.click_distribution.sample() / 1000.0
            time.sleep(dt)
            mouse_left_click()
            #mouse_up(button='left')
            #time.sleep(0.01)
            #mouse_down(button='left')
        # TODO: random move
    
    def right_click(self, n_clicks: int = 1):
        for i in range(n_clicks):
            dt = self.click_distribution.sample() / 1000.0
            time.sleep(dt)
            mouse_right_click()
        # TODO: random move
    
    def wait(self, n_seconds: float, p: float = 0.5):
        if random.random() < p:
            time.sleep(n_seconds)
        else:
            time.sleep(n_seconds) # TODO: random moves
