# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse, MouseMode
from rmm.simulator import Simulator

import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=[MouseMode.TRACKPAD, MouseMode.MOUSE])
    args = parser.parse_args()
        
    mouse = RealisticMouse(mode=args.mode)
    simulator = Simulator(mouse)
    simulator.simulate()