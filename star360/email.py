"""
Mail merge login credentials to a group of students, which must be done at the
start of a star360 test.
"""
import csv
from datetime import datetime
import sys
from pathlib import Path
import logging
from time import sleep

from teacherHelper import Helper, Email

logging.basicConfig(
    filename=Path(Path(__file__).parent, "star360_emailer.log"),
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

helper = Helper.read_cache()

class StudentNotFound(Exception):
    pass

class Star360MailMerge:

    def __init__(self, csv_path: Path, debug=True, skip=None):
        self.debug = debug   # sends all emails to me
        self.DEBUG_EMAIL = 'jdevries3133@gmail.com'
        self.csv = csv_path

        # allow the ability to skip some students on a second run after smtp
        # kick. This should be a list of exact-match student names.
        self.skip = skip if skip else []
        self.sent_to = []  # successfully sent; a list of names

        # saving myself from myself
        if not self.debug:
            i = input('WARNING: Really send emails to students?')
            if i != 'yes':
                print(f'input "{i}" != "yes". Exiting...')
                sys.exit()

        self.students = []
        with open(csv_path, 'r') as csvf:
            rd = csv.reader(csvf)

            # check on headers
            assert next(rd) == ['name', 'username', 'password']
            for name, username, password in rd:
                st = helper.find_nearest_match(name, auto_yes=True)
                if not st:
                    raise StudentNotFound(f'{name} not found')
                st.username = username
                st.password = password
                # LIMIT RECIPIENTS TO THE FOURTH GRADE.
                if (
                    st.grade_level == 4
                    and not st.homeroom == ['DAmario, Danielle','McNeill, Kaity']
                ):
                        self.students.append(st)

    def send_emails(self):
        # TODO: break up this big function
        sent_to = []
        with Email() as eml:
            for i, st in enumerate(self.students):
                if st.name in self.skip:
                    continue
                if self.debug:
                    recipient = self.DEBUG_EMAIL
                else:
                    recipient = st.email
                message = [
                    f'Hi {st.first_name},',
                    '',
                    'Today, you will be taking your Star360 Assessment. '
                    'Please complete the steps below:',
                    '',
                    '1. Click on this link: <a href="https://global-zone08.renaiss'
                    'ance-go.com/welcomeportal/6234531">https://global-zone08.rena'
                    'issance-go.com/welcomeportal/6234531</a>',
                    '2. Click "I\'m a Student"',
                    f'3. Type your Username: <b>{st.username}</b>',
                    f'4. Type your Password: <b>{st.password}</b>',
                    '5. Click "Log In"',
                    '6. Find the Star Math or Reading test (depending on teacher '
                    'directions).',
                    '7. Begin your test. If you need to enter a monitor password, '
                    'type <b>Admin</b>',
                    '8. When you finish, send a chat to your teacher.',
                    '',
                    '<span style="color: red;">STAY ON THE ZOOM UNTIL WE CONFIRM '
                    'YOU SUBMITTED YOUR TEST</span>',
                    '',
                    'Good luck!',
                ]
                eml.send(
                    to=recipient,
                    subject='Star360 Username and Password',
                    message=message
                )
                self.sent_to.append(st.name)
                logger.info(f'Email sent to {st.name} including username: {st.username}')
                logger.debug(f'{i}/{len(self.students)} emails sent')
                sent_to.append(st)
