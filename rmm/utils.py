# -*- coding: utf-8 -*-
# utils.py
# author: Antoine Passemiers

import pyautogui

import os


file_dir, _ = os.path.split(__file__)
DATA_PATH = os.path.join(file_dir, "data")


def get_screen_size():
    return tuple(pyautogui.size())


def get_mouse_position():
    return pyautogui.position()


def move_mouse_to(x, y):
    return pyautogui.platformModule._moveTo(int(x), int(y))


def mouse_move_to_with_tweening(x, y, dt):
    pyautogui.moveTo(int(x), int(y), dt, pyautogui.easeInQuad)
