"""
Finale does not allow you to copy and paste to duplicate an image :/
This script just repeatedly inserts and resizes an image into a Finale
document.
"""
from time import sleep
import pyautogui as pg


pg.PAUSE = 0.4

for _ in range(24):
    pg.click(x=625, y=13)
    pg.click(x=651, y=85)
    sleep(1)
    pg.click(x=593, y=231)
    pg.click(x=1026, y=554)
    sleep(0.4)
    pg.click(x=222, y=394)
    pg.moveTo(x=449, y=505)
    pg.keyDown('shift')
    pg.dragTo(x=371, y=467, button='left')
    pg.keyUp('shift')
