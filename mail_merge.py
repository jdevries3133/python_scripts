from pathlib import Path
import csv
from copy import copy
import sys
from dataclasses import dataclass

import markdown
from bs4 import BeautifulSoup

from teacherHelper import Email
from teacherHelper.email_ import Message


@dataclass
class Config:
    subject = ("",)
    cc_emails = None  # must be string, currently (not list)
    template_path = Path(Path(__file__).parent, "template.md")
    data_path = Path(Path(__file__).parent, "data.csv")


with open(Config.template_path) as markdownf:
    template = markdownf.read()

with open("data.csv", "r") as csvf:
    rd = csv.reader(csvf)
    for student, ela, math, par_name, par_email in rd:

        student_first_name = student.strip().split(" ")[-1]

        tags = {
            "{{parent}}": par_name,
            "{{math_letter_grade}}": math,
            "{{ela_letter_grade}}": ela,
            "{{student_first_name}}": student_first_name,
        }

        markdown_text = copy(template)
        for tag, value in tags.items():
            markdown_text = markdown_text.replace(tag, value)

        message = Message(
            html := markdown.markdown(markdown_text),
            "".join(BeautifulSoup(html, features="lxml").findAll(text=True)),
        )

        with Email() as emailer:
            emailer.send(
                to=par_email.strip(),
                subject=Config.subject,
                message=message,
                cc=Config.cc_emails,
            )
            print(f"Email for {student_first_name} sent")
