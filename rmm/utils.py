# -*- coding: utf-8 -*-
# utils.py
# author: Antoine Passemiers

import pyautogui


def get_screen_size():
    return tuple(pyautogui.size())


def get_mouse_position():
    return pyautogui.position()


def move_mouse_to(x, y):
    return pyautogui.platformModule._moveTo(int(x), int(y))


def mouse_move_to_with_tweening(x, y, dt):
    pyautogui.moveTo(int(x), int(y), dt, pyautogui.easeInQuad)
