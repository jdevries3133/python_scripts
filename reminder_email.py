from teacherHelper import Helper, Email

helper = Helper.read_cache()

EMAIL_SUBJECT = 'Turn In Your Writing'

groupings = [
    {
        # JUST TURN IN
        'students': [
            # List students here.
            # DO NOT COMMIT STUDENT NAMES TO VERSION CONTROL.
        ],
        'msg_func': lambda st: ([
            f'Hi {st.first_name}',
            '',
            'This is a friendly reminder that you still need to TURN IN '
            'today\'s writing assignment. Your work looks very nice, but '
            'you will not get full credit unless you head back to google '
            'classroom and press the "Turn In," button!'
        ])
    },
    {
        # NEED TO FINISH
        'students': [
            # list students here
            # DO NOT COMMIT STUDENT NAMES TO VERSION CONTROL.
        ],
        'msg_func': lambda st: ([
            f'Hi {st.first_name}',
            '',
            'This is a friendly reminder that you need to finish your '
            'writing assignment today. You\'re off to a great start, but '
            'remember to complete your work, and most importantly, to press '
            'TURN IN when you are finished.'
        ])
    },
]

with Email() as emlr:
    for grouping in groupings:
        for st_name in grouping['students']:
            st = helper.find_nearest_match(st_name, auto_yes=True)
            emlr.send(
                to=st.email,
                subject=EMAIL_SUBJECT,
                message=grouping['msg_func'](st)
            )
