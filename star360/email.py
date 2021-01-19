"""
Mail merge login credentials to a group of students, which must be done at the
start of a star360 test.
"""
import csv
from datetime import datetime
import sys
from pathlib import Path
import logging

from teacherHelper import Helper, Email

logging.basicConfig(
    filename="star360_emailer.log",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

helper = Helper.read_cache()

class StudentNotFound(Exception):
    pass

class Star360MailMerge:

    def __init__(self, csv_path: Path, debug=True):
        self.debug = debug   # sends all emails to me
        self.DEBUG_EMAIL = 'jdevries3133@gmail.com'
        self.csv = csv_path

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
                self.students.append(st)

    def send_emails(self):
        # TODO: break up this big function
        sent_to = []
        try:
            with Email() as eml:
                for st in self.students:
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
                    eml.send(
                        to=recipient,
                        subject='Star360 Username and Password',
                        message=message
                    )
                    logger.info(f'Email sent to {st.name} including username\t{st.onc}')
                    sent_to.append(st)
        except Exception as e:
            logger.critical(f'Program crashed due to {e}')
            with open(f'sent {datetime.now()}.csv', 'w') as csvf:
                wr = csv.writer(csvf)
                for st in sent_to:
                    wr.writerow((st.name,))
            print(
                'Program crashed. See logs for details. Students who recieved '
                'an email have been saved in ./sent.csv'
            )
            sys.exit()
