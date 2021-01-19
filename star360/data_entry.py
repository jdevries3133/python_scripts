import csv
import re

import pyperclip as pc
from teacherHelper import Helper

helper = Helper.read_cache()


def entry():
    """
    Take the data off each page from the clipboard and also do a first
    round of cleaning.
    """
    with open('out.csv', 'w') as csvf:
        while True:
            appends = {'a': [], 'b': [], 'c': []}
            append_to = 'a'
            for d in pc.paste().split('\n'):
                if d == 'User Name':
                        append_to = 'b'
                        continue
                if d == 'Grade Password':
                        append_to = 'c'
                        continue
                appends[append_to].append(d)

            wr = csv.writer(csvf)
            data = []
            for i in range(len(appends['a'])):
                last, first, *rest = appends['a'][i].split(',')
                row = [
                    f'{first} {last}',
                    appends['b'][i],
                    appends['c'][i],
                ]
                # clean names
                if not helper.find_nearest_match(row[0], auto_yes=True):
                    inp = input(f'Fix name "{row[0]}... {rest if rest else ""}" or press enter to keep: ')
                    row[0] = inp if inp else row[0]
                wr.writerow(row)
            inp = input('Enter to append again, or type "exit" to exit: ')
            if inp.lower() == 'exit':
                break

def _clean_name(name: str) -> str:
    if ',' in name:
        last, first, *rest = name.split(',')
        name = f'{first} {last}'
    st = helper.find_nearest_match(name, auto_yes=True)
    if not st:
        print(f'Warning! {name} was not found!')
    return st.name if st else name

def _clean_pwd(pwd: str) -> str:
    return re.search(
        r'Grade \d (.*)',
        pwd
    )[1]

def _clean_row(row: list) -> list:
    """
    Thoroughly clean each individual row.
    """
    row = [i.strip() for i in row]
    row[0] = _clean_name(row[0])
    row[2] = _clean_pwd(row[2])
    return row



def clean():
    cleaned = []
    with open('out.csv', 'r') as csvf:
        rd = csv.reader(csvf)
        for row in rd:
            cleaned.append(_clean_row(row))

    with open('clean.csv', 'w') as csvf:
        wr = csv.writer(csvf)
        wr.writerows(cleaned)

if __name__ == '__main__':
    clean()
