# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse, MouseMode
from rmm.simulator import Simulator
from rmm.shape import Polyline, Polygon, Shape

import argparse



def test_polygon():
    polyline = Polyline()
    polyline.add(500, 300)
    polyline.add(600, 300)
    polyline.add(600, 400)
    polyline.add(700, 400)
    polyline.add(700, 500)
    polyline.add(600, 500)
    polyline.add(600, 600)
    polyline.add(500, 600)
    polyline.add(500, 500)
    polyline.add(400, 500)
    polyline.add(400, 400)
    polyline.add(500, 400)
    polyline.stop()

    polygon = Polygon(polyline)

    mouse = RealisticMouse()
    while True:
        mouse.move_to(polygon)
        mouse.click()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=[MouseMode.TRACKPAD, MouseMode.MOUSE])
    args = parser.parse_args()
        
    mouse = RealisticMouse(mode=args.mode)
    simulator = Simulator(mouse)
    simulator.simulate()
