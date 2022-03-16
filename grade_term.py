"""Grade term projects"""

from time import sleep
import pyautogui as pg


def hotkey(*keys):
    pg.hotkey(*keys)


def goto_slide(name):
    orig = pg.PAUSE
    pg.PAUSE = 0.3
    # focus the outer iframe
    pg.click(x=682, y=204)
    # click on the dropdown
    pg.click(x=367, y=204)
    # search for the student
    hotkey("command", "f")
    pg.typewrite(name)
    pg.press("enter")
    # click on that student's slides
    pg.click(x=366, y=468)
    # give slides a moment to load
    sleep(0.4)
    # focus the inner iframe with the slides
    pg.click(x=90, y=319)
    pg.PAUSE = orig


def wait_for_input():
    input("press enter to continue")
    # go back to previous program
    hotkey("command", "tab")


def main():
    student = input("enter student: ")
    hotkey("command", "tab")

    # week 19 slide
    goto_slide(student)

    for _ in range(7):
        pg.press("down")

    wait_for_input()

    # week 20 do-now's part 1 and 2
    for _ in range(2):
        hotkey("ctrl", "shift", "tab")
        goto_slide(student)
        pg.press("down")

        wait_for_input()

    # week 21 google forms
    for _ in range(2):
        hotkey("ctrl", "shift", "tab")
        hotkey("command", "f")
        pg.typewrite(student)
        pg.press("enter")

        wait_for_input()


if __name__ == "__main__":
    while True:
        main()
