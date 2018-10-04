# -*- coding: utf-8 -*-
# utils.py
# author: Antoine Passemiers

import pyautogui
try:
    from mss import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

import ctypes
import platform
import os
import json
import zipfile


file_dir, _ = os.path.split(__file__)
DATA_PATH = os.path.join(file_dir, 'data')
MV_FILE_PATH = os.path.join(DATA_PATH, 'movements.zip')
SPECIAL_FILE_PATH = os.path.join(DATA_PATH, 'special.zip')
CLICK_FILE_PATH = os.path.join(DATA_PATH, 'click_diffs.npy')

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
    return x, y


def requires_mss(func):
    def new_func(*args, **kwargs):
        if MSS_AVAILABLE:
            return func(*args, **kwargs)
        else:
            raise ImportError(
                'MSS should be installed in order to use this function.')
    return new_func


if platform.system() == 'Windows':
    def __move_to(x, y):
        ctypes.windll.user32.SetCursorPos(x, y)
else:
    raise NotImplementedError()


@requires_mss
def get_monitor_coords():
    with mss() as sct:
        coords = sct.monitors
    return coords


def move_mouse_to(x, y, multi_monitor=False):
    x, y = int(round(x)), int(round(y))
    if not multi_monitor:
        x, y = remove_screen_overflow(x, y)
        pyautogui.platformModule._moveTo(x, y)
    else:
        __move_to(int(x), int(y))


def mouse_move_to_with_tweening(x, y, dt):
    x, y = remove_screen_overflow(x, y)
    pyautogui.moveTo(x, y, dt, pyautogui.easeInQuad)


def mouse_left_click():
    pyautogui.click()


def mouse_right_click():
    pyautogui.click(button='right')


def get_mouse_data(filepath):
    if os.path.isfile(filepath):
        with zipfile.ZipFile(filepath, "r", zipfile.ZIP_DEFLATED) as z:
            assert(len(z.namelist()) == 1)
            filename = z.namelist()[0]
            with z.open(filename) as f:
                data = json.loads(f.read().decode('utf-8'))
    else:
        # TODO: raise exception
        pass
    return data


def get_mv_data():
    return get_mouse_data(MV_FILE_PATH)


def get_special_data():
    return get_mouse_data(SPECIAL_FILE_PATH)


class NoDataFoundException(Exception):
    pass