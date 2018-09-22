# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse, MouseMode
from rmm.simulator import Simulator
from rmm.shape import Polyline, Polygon, Shape

import argparse


"""
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=[MouseMode.TRACKPAD, MouseMode.MOUSE])
    args = parser.parse_args()
        
    mouse = RealisticMouse(mode=args.mode)
    simulator = Simulator(mouse)
    simulator.simulate()
"""

if __name__ == '__main__':
    polyline = Polyline()
    polyline.add(500, 500)
    polyline.add(1000, 500)
    polyline.add(500, 700)
    """
    polyline.add(1, 2)
    polyline.add(1, 5)
    polyline.add(0, 5)
    """
    polyline.stop()

    polygon = Polygon(polyline)

    mouse = RealisticMouse()
    for i in range(1000):
        mouse.move_to(polygon)
        mouse.click()
