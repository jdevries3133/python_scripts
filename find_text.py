import os
import sys
import logging

import pyautogui as pg
import cv2
import pytesseract

from utils import plural

logger = logging.getLogger(__name__)

def main(text):
    print(f'Searching for text {text} on the screen...')
    data = ''
    n = 0
    while not text in data:
        if n:
            print(
                f'{text} was not found on the screen in the {plural(n)} search'
            )
        n += 1

        pg.screenshot().save('temp.png')

        # Grayscale, Gaussian blur, Otsu's threshold
        image = cv2.imread('temp.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        # Perform text extraction
        data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        data = data.lower()


    print('TEXT FOUND')
    os.remove('temp.png')

if __name__ == '__main__':
    logging.basicConfig(handlers=(logging.StreamHandler(),), level=logging.ERROR)
    main(sys.argv[1] if len(sys.argv) >= 2 else 'search result')
