"""
Send mass email to a group of students, which must be done at the start of
a star360 test.
"""
import csv
from datetime import datetime
import os

from teacherHelper import Helper, Email

# define global constants
DEBUG = True  # send emails to me 
if DEBUG:
    print('Running in DEBUG mode.')
ALL_4 = False  # send to the whole grade, not just katelyn's class
(
    print('Sending to all 4th grade')
    if ALL_4
    else print('Sending to Mrs. Geltzeiler\'s class.')
)

passwd = os.getenv('STAR460_STUDENT_PASS')
helper = Helper.read_cache()


def select_students() -> dict:
    """
    Create the students dict based on the global constants. Create generic
    oncourse usernames and passwords without regard for exceptions.
    """
    students = {}
    # deal with most of the grade
    for st in helper.students.values():
        # other grades are a dumpster fire of inconsistencies for some reason.
        if st.grade_level != 4:
            continue
        if st.homeroom != 'Geltzeiler, Katelyn' and not ALL_4:
            continue
        if '-' in st.last_name:
            p1, p2 = st.last_name.split('-')
            st.onc = (st.first_name[0] + p1 + p2[0]).lower()
        else:
            st.onc = (st.first_name[0] + st.last_name).lower()
        st.passwd = passwd
        students.setdefault(st.name, st)
    return students

def _fix_exceptions(students: dict) -> dict:
     # handle the exceptions with different usernames
    with open('exceptions.csv', 'r', encoding='utf-8-sig') as csvf:
        rd = csv.reader(csvf, dialect='excel')
        for row in rd:
            st = students.get(row[0])
            if not st:
                continue
            st.onc = row[1]
            st.passwd = passwd
    return students

def send_emails(students: dict):
    with Email() as eml:
        for st in students.values():
            if DEBUG:
                recipient = 'jdevries3133@gmail.com'
            else:
                recipient = st.email
            message = [
                'Ok, all is working well now: here is a sample email',

                '',

                f'Hi {st.first_name},',

                '',

                'Today, you will be taking your Star360 Assessment. '

                'Please complete the steps below:',

                '',

                '1. Click on this link: <a href="https://global-zone08.renaiss'
                'ance-go.com/welcomeportal/6234531">https://global-zone08.rena'
                'issance-go.com/welcomeportal/6234531</a>',

                '2. Click "I\'m a Student"',

                f'3. Type your Username: {st.onc}',

                f'4. Type your Password: {st.passwd}',

                '5. Click "Log In"',

                '6. Find the Star Math or Reading test (depending on teacher '
                'directions).',

                '7. Begin your test. If you need to enter a monitor password, '
                'type <b>Admin</b>',

                '',

                '<span style="color: red;">STAY ON THE ZOOM UNTIL WE CONFIRM '
                'YOU SUBMITTED YOUR TEST</span>',

                '',

                'Good luck!',
            ]
            if not DEBUG:
                eml.send(
                    to=recipient,
                    subject='Star360 Login Information',
                    message=message
                )
            print(f'Email sent to {st.name} including username\t{st.onc}')

def save_data_sent(students: dict) -> None:
    students = sorted([s for s in students.values()], key=lambda i: i.homeroom)  # type: ignore
    with open(f'sent {datetime.now()}.csv', 'w') as csvf:
        wr = csv.writer(csvf)
        wr.writerow(['Name', 'Username', 'Password', 'Homeroom'])
        for st in students:
            wr.writerow([st.name, st.onc, st.passwd, st.homeroom])

def main():
    students = select_students()
    students = _fix_exceptions(students)
    save_data_sent(students)
    send_emails(students)

if __name__ == '__main__':
    main()
