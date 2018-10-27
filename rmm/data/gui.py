# -*- coding: utf-8 -*-
# gui.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse
from rmm.movement import *
from rmm.utils import *

import os
import copy
import zipfile
import json
import argparse
import numpy as np
import scipy.interpolate
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class GUI:

    def __init__(self, action):
        self.click_movements = list()
        self.wait_movements = list()
        self.movements = list()
        self.blue_pressed = self.red_pressed = True
        self.src = self.dest = None

        self.master = tk.Tk()
        self._geom = '200x200+0+0'
        self.width = self.master.winfo_screenwidth() - 3
        self.height = self.master.winfo_screenheight() - 3
        self.master.geometry("{0}x{1}+0+0".format(self.width, self.height))

        self.button_size = 10
        self.button_blue = tk.Button(self.master, command=self.on_click_blue, bg='blue')
        self.button_blue.config(height=self.button_size, width=self.button_size*2)
        self.button_red = tk.Button(self.master, command=self.on_click_red, bg='red')
        self.button_red.config(height=self.button_size, width=self.button_size*2)

        self.last_click = None
        self.click_time_diffs = []
        self.button_green = tk.Button(self.master, command=self.on_click_green, bg='green')
        self.button_green.config(height=20, width=20*2)

        if action == 'move':
            self.place_buttons()
        elif action == 'wait':
            pass

        self.master.mainloop()          
    
    def random_coords(self, pad=100):
        x = np.random.randint(pad, self.width-pad)
        y = np.random.randint(pad, self.height-pad)
        return x, y
    
    def place_green_button(self):
        self.button_green.place_forget()
        self.button_green.place(x=500, y=200)
    
    def on_click_green(self):
        click = MouseMovement.time_millis()
        if self.last_click is not None:
            if click - self.last_click < 500.0:
                diff = int(click - self.last_click)
                self.click_time_diffs.append(diff - (diff % 5))
        self.last_click = click

    def place_buttons(self):
        self.button_red.place_forget()
        self.button_blue.place_forget()

        self.button_size = int(np.random.randint(1, 25))
        x, y = self.random_coords()
        self.button_blue.config(height=self.button_size, width=self.button_size*2)
        self.button_blue.place(x=x, y=y)
        self.src = (x, y)
        x, y = self.random_coords()
        self.button_red.config(height=self.button_size, width=self.button_size*2)
        self.button_red.place(x=x, y=y)
        self.dest = (x, y)
        self.blue_pressed = self.red_pressed = False
    
    def on_click_blue(self):
        if self.red_pressed:
            self.movements[-1].stop_recording()
            self.movements[-1].aod = self.button_size
            self.blue_pressed = True
            self.place_buttons()
    
    def on_click_red(self):
        self.button_red.place_forget()
        self.red_pressed = True
        self.movements.append(MouseMovement())
        self.movements[-1].start_recording()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['mouse', 'trackpad'])
    parser.add_argument("action", choices=['move', 'click', 'wait'])
    args = parser.parse_args()

    data = get_mv_data()
    print(len(data[args.mode]))

    gui = GUI(args.action)
    data[args.mode] += [movement.__dict__() for movement in gui.movements]

    src_json_path = os.path.join(os.path.split(__file__)[0], 'movements.json')
    json_file = open(src_json_path, "w")
    json.dump(data, json_file)
    json_file.close()

    src_mv_path = os.path.join(os.path.split(__file__)[0], 'movements.zip')
    with zipfile.ZipFile(src_mv_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(src_json_path)
    os.remove(src_json_path)
