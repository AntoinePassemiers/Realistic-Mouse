# -*- coding: utf-8 -*-
# movement.py
# author: Antoine Passemiers

from typing import Dict, Any

from rmm.utils import *

import numpy as np
import time
import threading


class MouseMovement:

    def __init__(self):
        self.coords = []
        self.timestamps = []
        self.last = None
        self.recording = False
        self.aod = None
    
    @staticmethod
    def time_millis() -> int:
        return int(round(time.time() * 1000.))

    def record_current_position(self):
        current = get_mouse_position()
        if current != self.last:
            self.coords.append(current)
            self.timestamps.append(MouseMovement.time_millis())
        self.last = current
    
    def record(self):
        while self.recording:
            self.record_current_position()
    
    def start_recording(self):
        self.recording = True
        t = threading.Thread(target=self.record)
        t.start()
    
    def stop_recording(self):
        self.recording = False
    
    def replay(self, backend, speed: float = 1., multi_monitor: bool = False):
        pauses = np.insert(np.diff(self.timestamps), 0, 0, axis=0)
        pauses = np.round(pauses / speed).astype(int)
        t1 = MouseMovement.time_millis()
        for i in range(len(self.coords)):
            t2 = MouseMovement.time_millis()
            duration = pauses[i] - (t2 - t1)
            if duration > 0:
                time.sleep(float(duration) / 1000.)
            x, y = self.coords[i]
            t1 = MouseMovement.time_millis()
            move_mouse_to(backend, x, y, multi_monitor=multi_monitor)
    
    @staticmethod
    def linear_tweening(backend, x1: int, y1: int, t: float = 0.3, multi_monitor: bool = False):
        x0, y0 = get_mouse_position()
        dt = 0.01
        for ct in np.arange(0, t, dt):
            alpha = float(ct) / t
            x = alpha * x1 + (1. - alpha) * x0
            y = alpha * y1 + (1. - alpha) * y0
            t1 = MouseMovement.time_millis()
            move_mouse_to(backend, x, y, multi_monitor=multi_monitor)
            t2 = MouseMovement.time_millis()
            duration = dt - (t2 - t1)
            if duration > 0:
                time.sleep(float(duration) / 1000.)
        move_mouse_to(backend, x1, y1, multi_monitor=multi_monitor)
    
    def __iadd__(self, c):
        x, y = c
        self.coords = list(np.asarray(self.coords) + np.asarray([x, y]))
        return self
    
    def __isub__(self, c):
        x, y = c
        self.coords = list(np.asarray(self.coords) - np.asarray([x, y]))
        return self

    def __sub__(self, c):
        x, y = c
        new_movement = MouseMovement()
        new_movement.last = self.last
        new_movement.recording = self.recording
        new_movement.timestamps = self.timestamps
        new_movement.coords = list(np.asarray(self.coords) - np.asarray([x, y]))
        return new_movement
    
    def __len__(self) -> int:
        return len(self.coords)
    
    def __dict__(self) -> Dict[str, Any]:
        return {
            'aod': self.aod,
            'screen_resolution': SCREEN_RESOLUTION,
            'coords': [[int(x), int(y)] for x, y in self.coords],
            'timestamps': [int(d) for d in list(np.asarray(self.timestamps) - self.timestamps[0])]}
    
    @staticmethod
    def from_dict(d) -> 'MouseMovement':
        movement = MouseMovement()
        screen_resolution = d['screen_resolution']  # TODO
        movement.coords = d['coords']
        movement.timestamps = d['timestamps']
        if 'aod' in d.keys():
            movement.aod = d['aod']
        return movement
