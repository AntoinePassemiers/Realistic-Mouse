# -*- coding: utf-8 -*-
# move.py
# author: Antoine Passemiers

from rmm.movement import MouseMovement

import numpy as np
import pyautogui
import os
import copy
import random
import argparse
import time
import threading
import json
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class GUI:

    def __init__(self):
        self.movements = list()
        self.blue_pressed = self.red_pressed = True
        self.src = self.dest = None

        self.master = tk.Tk()
        self._geom = '200x200+0+0'
        self.width = self.master.winfo_screenwidth() - 3
        self.height = self.master.winfo_screenheight() - 3
        self.master.geometry("{0}x{1}+0+0".format(self.width, self.height))

        button_size = 2
        self.button_blue = tk.Button(self.master, command=self.on_click_blue, bg='blue')
        self.button_blue.config(height=button_size, width=button_size*2)
        self.button_red = tk.Button(self.master, command=self.on_click_red, bg='red')
        self.button_red.config(height=button_size, width=button_size*2)

        self.place_buttons()

        self.master.mainloop()
    
    def random_coords(self, pad=100):
        x = np.random.randint(pad, self.width-pad)
        y = np.random.randint(pad, self.height-pad)
        return x, y

    def place_buttons(self):
        self.button_red.place_forget()
        self.button_blue.place_forget()
        x, y = self.random_coords()
        self.button_blue.place(x=x, y=y)
        self.src = (x, y)
        x, y = self.random_coords()
        self.button_red.place(x=x, y=y)
        self.dest = (x, y)
        self.blue_pressed = self.red_pressed = False
    
    def on_click_blue(self):
        if self.red_pressed:
            print(len(self.movements))
            self.movements[-1].stop_recording()
            self.blue_pressed = True
            self.place_buttons()
    
    def on_click_red(self):
        self.button_red.place_forget()
        self.red_pressed = True
        self.movements.append(MouseMovement())
        self.movements[-1].start_recording()
    

class Simulator:

    def __init__(self, mouse):
        self.mouse = mouse
    
    def simulate(self):
        while True:
            x, y = self.random_coords()
            self.mouse.move_to(x, y)

    def random_coords(self):
        x = np.random.randint(0, MouseMovement.SCREEN_RESOLUTION[0])
        y = np.random.randint(0, MouseMovement.SCREEN_RESOLUTION[1])
        return x, y
