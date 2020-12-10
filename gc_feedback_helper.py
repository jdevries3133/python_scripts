from time import sleep

import pyperclip as pc
import pyautogui as pg
from teacherHelper import Helper

pg.PAUSE = 0.3

def main():
    students = Helper.read_cache().homerooms['Geltzeiler, Katelyn'].students
    students.sort(key=lambda s: s.first_name)
    for st in students[5:]:
        print(f'Current student: {st.name}')
        try:
            insert = input('Insert: ').title()
            feedback = (
                f'Great job {st.first_name}! Your story about the {insert} is '
                'very funny and a pleasure to read.'
            )
            pc.copy(feedback)
            pg.hotkey('command', 'tab')
            pg.click(x=1249, y=498)
            pg.typewrite('100')
        except KeyboardInterrupt:
            continue

def get_position_infinite():
    while True:
        print(pg.position())
        input()



if __name__ == '__main__':
    main()
