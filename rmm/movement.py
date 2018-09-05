# -*- coding: utf-8 -*-
# movement.py
# author: Antoine Passemiers

from rmm.utils import *

import numpy as np
import time
import threading


class MouseMovement:

    SCREEN_RESOLUTION = get_screen_size()

    def __init__(self):
        self.coords = list()
        self.timestamps = list()
        self.last = None
        self.recording = False
    
    def time_millis(self):
        return int(round(time.time() * 1000.))

    def record_current_position(self):
        current = get_mouse_position()
        if current != self.last:
            self.coords.append(current)
            self.timestamps.append(self.time_millis())
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
    
    def replay(self):
        pauses = np.diff(self.timestamps) / 1000.
        x, y = self.coords[0]
        move_mouse_to(x, y)
        for i in range(len(self.coords)-1):
            time.sleep(pauses[i])
            x, y = self.coords[i+1]
            move_mouse_to(x, y)
    
    def __iadd__(self, c):
        x, y = c
        self.coords = list(np.asarray(self.coords) + np.asarray([x, y]))
        return self
    
    def __isub__(self, c):
        x, y = c
        self.coords = list(np.asarray(self.coords) - np.asarray([x, y]))
        return self
    
    def __len__(self):
        return len(self.coords)
    
    def __dict__(self):
        return {
            'screen_resolution': MouseMovement.SCREEN_RESOLUTION,
            'coords': [[int(x), int(y)] for x, y in self.coords],
            'timestamps': [int(d) for d in list(np.asarray(self.timestamps) - self.timestamps[0])]}
    
    @staticmethod
    def from_dict(d):
        movement = MouseMovement()
        screen_resolution = d['screen_resolution'] # TODO
        movement.coords = d['coords']
        movement.timestamps = d['timestamps']
        return movement
