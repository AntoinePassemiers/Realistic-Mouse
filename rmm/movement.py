# -*- coding: utf-8 -*-
# movement.py
# author: Antoine Passemiers

from rmm.utils import *

import numpy as np
import time
import threading


class MouseMovement:

    def __init__(self):
        self.coords = list()
        self.timestamps = list()
        self.last = None
        self.recording = False
    
    @staticmethod
    def time_millis():
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
    
    def replay(self, multi_monitor=False):
        pauses = np.diff(self.timestamps)
        x, y = self.coords[0]
        t1 = MouseMovement.time_millis()
        move_mouse_to(x, y, multi_monitor=multi_monitor)
        for i in range(len(self.coords)-1):
            t2 = MouseMovement.time_millis()
            duration = pauses[i] - (t2 - t1)
            # assert(duration >= 0)
            if duration > 0:
                time.sleep(float(duration) / 1000.)
            x, y = self.coords[i+1]
            t1 = MouseMovement.time_millis()
            move_mouse_to(x, y, multi_monitor=multi_monitor)
    
    @staticmethod
    def linear_tweening(x1, y1, multi_monitor=False):
        x0, y0 = get_mouse_position()
        distance = np.sqrt((x1 - x0) ** 2. + (y1 - y0) ** 2.)
        t = 0.3 # TODO
        dt = 0.01
        for ct in np.arange(0, t, dt):
            alpha = float(ct) / t
            x = alpha * x1 + (1. - alpha) * x0
            y = alpha * y1 + (1. - alpha) * y0
            t1 = MouseMovement.time_millis()
            move_mouse_to(x, y, multi_monitor=multi_monitor)
            t2 = MouseMovement.time_millis()
            duration = dt - (t2 - t1)
            if duration > 0:
                time.sleep(float(duration) / 1000.)
        move_mouse_to(x1, y1, multi_monitor=multi_monitor)
    
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
    
    def __len__(self):
        return len(self.coords)
    
    def __dict__(self):
        return {
            'screen_resolution': SCREEN_RESOLUTION,
            'coords': [[int(x), int(y)] for x, y in self.coords],
            'timestamps': [int(d) for d in list(np.asarray(self.timestamps) - self.timestamps[0])]}
    
    @staticmethod
    def from_dict(d):
        movement = MouseMovement()
        screen_resolution = d['screen_resolution'] # TODO
        movement.coords = d['coords']
        movement.timestamps = d['timestamps']
        return movement
