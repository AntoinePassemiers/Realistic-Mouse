# Realistic mouse for building undetectable click bots

## How to use it

```python
>>> from rmm.mouse import RealisticMouse, MouseMode
>>> mouse = RealisticMouse(mode=MouseMode.TRACKPAD)
>>> x, y = 824, 365 # Destination coordinates
>>> mouse.move_to(x, y)
>>> mouse.left_click()
>>> mouse.right_click()
```

## Installation

From the parent folder, install the library by entering the following command:

```sh
$ sudo python setup.py install
```

### Dependencies

* numpy >= 1.13.3
* pyautogui
