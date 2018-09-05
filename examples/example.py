# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse
from rmm.move import *
from rmm.utils import DATA_PATH

import os
import copy
import json
import argparse
import pyautogui


if __name__ == '__main__':

    MV_FILE_PATH = os.path.join(DATA_PATH, 'movements.json')

    pyautogui.FAILSAFE = False # TODO

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['mouse', 'trackpad', 'simulate'])
    args = parser.parse_args()

    print(MV_FILE_PATH)

    if os.path.isfile(MV_FILE_PATH):
        json_file = open(MV_FILE_PATH, "r")
        data = json.load(json_file)
        json_file.close()
    else:
        data = {'mouse': [], 'trackpad': []}

    if args.mode != 'simulate':
        gui = GUI()
        data[args.mode] += [movement.__dict__() for movement in gui.movements]
    else:
        movements = copy.deepcopy(data)
        for mode in ['trackpad', 'mouse']:
            for i in range(len(movements[mode])):
                movements[mode][i] = MouseMovement.from_dict(movements[mode][i])
            
        print(MouseMovement.SCREEN_RESOLUTION)

        mouse = RealisticMouse(movements)
        simulator = Simulator(mouse)
        simulator.simulate()

    json_file = open(MV_FILE_PATH, "w")
    json.dump(data, json_file)
    json_file.close()
