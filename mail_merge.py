from pathlib import Path
import csv
from copy import copy
import sys

import markdown
from bs4 import BeautifulSoup

from teacherHelper import Email
from teacherHelper.email_ import Message


with open('template.md') as markdownf:
    template = markdownf.read()

with open('data.csv', 'r') as csvf:
    rd = csv.reader(csvf)
    rows = [r for r in rd]
    rows = rows[8:]
    for student, ela, math, par_name, par_email in rows:

        student_first_name = student.strip().split(' ')[-1]

        tags = {
            '{{parent}}': par_name,
            '{{math_letter_grade}}': math,
            '{{ela_letter_grade}}': ela,
            '{{student_first_name}}': student_first_name
        }

        markdown_text = copy(template)
        for tag, value in tags.items():
            markdown_text = markdown_text.replace(tag, value)

        message = Message(
            html := markdown.markdown(markdown_text),
            ''.join(BeautifulSoup(html, features='lxml').findAll(text=True))
        )

        with Email() as emailer:
            print(f'Email for {student_first_name} sent')
            emailer.send(
                to=par_email.strip(),
                subject=f'{student_first_name}\'s ELA and Math Progress',
                message=message,
                cc='kgeltzeiler@empacad.org',
            )
