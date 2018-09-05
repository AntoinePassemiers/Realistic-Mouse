# -*- coding: utf-8 -*-
# utils.py
# author: Antoine Passemiers

import pyautogui

import os
import json


file_dir, _ = os.path.split(__file__)
DATA_PATH = os.path.join(file_dir, 'data')
MV_FILE_PATH = os.path.join(DATA_PATH, 'movements.json')

pyautogui.FAILSAFE = False # TODO
SCREEN_RESOLUTION = tuple(pyautogui.size())


def get_screen_size():
    return tuple(pyautogui.size())


def get_mouse_position():
    return pyautogui.position()


def remove_screen_overflow(x, y):
    if x < 0:
        x = 0
    elif x >= SCREEN_RESOLUTION[0]:
        x = SCREEN_RESOLUTION[0] # TODO
    if y < 0:
        y = 0
    elif y >= SCREEN_RESOLUTION[1]:
        y = SCREEN_RESOLUTION[1] # TODO
    x, y = int(x), int(y)
    return x, y


def move_mouse_to(x, y):
    x, y = remove_screen_overflow(x, y)
    pyautogui.platformModule._moveTo(x, y)


def mouse_move_to_with_tweening(x, y, dt):
    x, y = remove_screen_overflow(x, y)
    pyautogui.moveTo(x, y, dt, pyautogui.easeInQuad)


def get_mv_data():
    if os.path.isfile(MV_FILE_PATH):
        json_file = open(MV_FILE_PATH, "r")
        data = json.load(json_file)
        json_file.close()
    else:
        # TODO: raise exception
        pass
    return data


class NoDataFoundException(Exception):
    pass