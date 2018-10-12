# -*- coding: utf-8 -*-
# example.py
# author: Antoine Passemiers

from rmm.mouse import RealisticMouse, MouseMode
from rmm.simulator import Simulator
from rmm.shape import Polyline, Polygon, Shape, Circle

import argparse
import numpy as np
import matplotlib.pyplot as plt


def test_circle():
    circle = Circle(800, 600, 15)
    x, y = list(), list()
    for i in range(2000):
        point = circle.sample()
        x.append(point[0])
        y.append(point[1])
    plt.switch_backend('TKAgg')
    plt.scatter(x, y)
    plt.show()


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


def simulate():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=[MouseMode.TRACKPAD, MouseMode.MOUSE])
    args = parser.parse_args()
        
    mouse = RealisticMouse(mode=args.mode)
    simulator = Simulator(mouse)
    simulator.simulate()


if __name__ == '__main__':
    test_circle()
