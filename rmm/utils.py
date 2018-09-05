# -*- coding: utf-8 -*-
# utils.py
# author: Antoine Passemiers

import pyautogui

import os
import json
import zipfile


file_dir, _ = os.path.split(__file__)
DATA_PATH = os.path.join(file_dir, 'data')
MV_FILE_PATH = os.path.join(DATA_PATH, 'movements.zip')

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
        x = SCREEN_RESOLUTION[0]-1
    if y < 0:
        y = 0
    elif y >= SCREEN_RESOLUTION[1]:
        y = SCREEN_RESOLUTION[1]-1
    x, y = int(x), int(y)
    return x, y


def move_mouse_to(x, y):
    x, y = remove_screen_overflow(x, y)
    pyautogui.platformModule._moveTo(x, y)


def mouse_move_to_with_tweening(x, y, dt):
    x, y = remove_screen_overflow(x, y)
    pyautogui.moveTo(x, y, dt, pyautogui.easeInQuad)


def mouse_left_click():
    pyautogui.click()


def mouse_right_click():
    pyautogui.click(button='right')


def get_mv_data():
    if os.path.isfile(MV_FILE_PATH):
        with zipfile.ZipFile(MV_FILE_PATH, "r", zipfile.ZIP_DEFLATED) as z:
            assert(len(z.namelist()) == 1)
            filename = z.namelist()[0]
            with z.open(filename) as f:
                data = json.loads(f.read())
    else:
        # TODO: raise exception
        pass
    return data


class NoDataFoundException(Exception):
    pass