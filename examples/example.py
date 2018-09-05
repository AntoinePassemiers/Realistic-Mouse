# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse
from rmm.move import *

import os
import copy
import json
import argparse
import pyautogui


if __name__ == '__main__':

    pyautogui.FAILSAFE = False # TODO

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['mouse', 'trackpad', 'simulate'])
    args = parser.parse_args()

    if os.path.isfile('movements.json'):
        json_file = open('movements.json', "r")
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

    json_file = open('movements.json', "w")
    json.dump(data, json_file, indent=4)
    json_file.close()
