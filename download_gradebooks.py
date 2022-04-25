from time import sleep

import pyautogui as pg
from pyautogui import Point


locations = [
    # class selector
    Point(x=558, y=196),
    # inserting some key presses here...
    "down",
    "enter",
    # actions
    Point(x=385, y=221),
    # export_to_excel
    Point(x=408, y=372),
    # confirm
    Point(x=828, y=645),
    # close modal
    Point(x=1037, y=368),
]


def hotkey(*args):
    for a in args:
        pg.keyDown(a)
    for a in args:
        pg.keyUp(a)


def main():
    """Iteratively click through to download all the gradebooks as csv files."""
    # focus on chrome
    hotkey("command", "space")
    pg.typewrite("chrome")
    pg.press("enter")

    for _ in range(20):
        for l in locations:
            if isinstance(l, str):
                pg.press(l)
                if l == "enter":
                    sleep(2)
                continue
            pg.click(*l)


if __name__ == "__main__":
    main()
