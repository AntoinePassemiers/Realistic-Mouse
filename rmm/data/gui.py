# -*- coding: utf-8 -*-
# gui.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse
from rmm.move import *
from rmm.utils import SCREEN_RESOLUTION, MV_FILE_PATH

import os
import copy
import json
import argparse
import numpy as np
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
            self.movements[-1].stop_recording()
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
    args = parser.parse_args()

    if os.path.isfile(MV_FILE_PATH):
        json_file = open(MV_FILE_PATH, "r")
        data = json.load(json_file)
        json_file.close()
    else:
        print('[WARNING] No data file found. New file created.')
        data = {'mouse': [], 'trackpad': []}

    gui = GUI()
    data[args.mode] += [movement.__dict__() for movement in gui.movements]

    src_mv_path = os.path.join(os.path.split(__file__)[0], 'movements.json')
    print(src_mv_path)

    json_file = open(src_mv_path, "w")
    json.dump(data, json_file)
    json_file.close()
