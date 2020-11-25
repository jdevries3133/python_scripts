import logging

import pyautogui as pg
import cv2
from teacherHelper import Helper
import pytesseract

# init helper
helper = Helper.read_cache()

# init logger
global_level = logging.INFO
sh = logging.StreamHandler()
sh.setLevel(global_level)
logging.getLogger('').setLevel(logging.ERROR)
logging.basicConfig(
    level=global_level,
    format='%(levelname)s: %(message)s',
    handlers=[sh],
)
logger = logging.getLogger(__name__)

# init pyautogui
pg.PAUSE = 1


all_ = ''
for _ in range(2):
    pg.screenshot(region=(115, 110, 500, 1430)).save(f'temp{_}.png')

    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(f'temp{_}.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

    # record results, scroll
    all_ += data
    pg.scroll(-15)


attendees = set()
logger.info('Zoom Name\tMatch')
unmatched = []
for line in all_.split('\n'):

    if 'layla' in line.lower():
        attendees.add(helper.students['Layla Johnson'])
        continue

    logger.debug(f'Raw line: {line}')

    # select second and third word
    name = ' '.join(line.split(' ')[1:3])

    if ' ' in name:
        # if the third word is (Guest), just use the second word alone.
        if name[name.index(' ') + 1] == '(':
            name = name.split(' ')[0]

    logger.debug(f'****** Searching for {name} ******')

    st = helper.exhaustive_search(
        name,
        helper.homerooms['Geltzeiler, Katelyn'].students,
        threshold=60
    )
    if not st:
        logger.info(f'{line}\t!!!!\tNO MATCH')
        unmatched.append(line.strip())
        continue
    logger.info(f'{line}\t=>\t{st.name}')
    if st:
        attendees.add(st)

print('** Unmatched Items **')
print('\n\t'.join(unmatched), '\n')

for st in helper.homerooms['Geltzeiler, Katelyn'].students:
    if st not in attendees:
        print(f'{st.name} is NOT in the zoom call!')
