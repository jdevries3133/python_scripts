"""
Assss a google classroom assignment with the pyautogc package.
"""
import os
from time import sleep

from pyautogc import FeedbackAutomatorBase


CHECK_SLIDE = 4


class CustomAutomator(FeedbackAutomatorBase):
    def assess(self):
        self.view_slide(CHECK_SLIDE)
        self.context['grade'] = self.user_input_grade()
        self.context['feedback'] = self.user_input_feedback()

    def user_input_grade(self):
        """
        Take fractional grade from user input
        """
        grade = input(f'Input grade for {self.context.get("name")}:\n')

        # validate user input
        try:
            self.context['grade'] = int(grade)
            if not self.is_grade_valid(self.context['grade']):
                print('Invalid grade')
                return self.user_input_grade()
        except ValueError:
            print('Invalid grade')
            return self.user_input_grade()
        return int(grade)

    def user_input_feedback(self):
        """
        Provide the list of feedback codes; user gives a feedback code
        or custom feedback. Custom feedback is re-printed and confirmed before
        moving on.
        """
        # get possible codes from comment bank by passing no args
        feedback_codes = "|".join(self.comment_bank())
        # user input feedback separately
        feedback = input(
            f'Enter feedback code ({feedback_codes}) or custom feedback: '
        )
        if feedback not in self.comment_bank():
            confirm = input(
                f'Entering custom feedback: {feedback}\n\nok? (y/n) '
            )
            if 'n' in confirm:
                print('Discarding custom feedback.')
                return self.user_input_feedback()
            return feedback
        return self.comment_bank(feedback)

    def comment_bank(self, feedback_code=None):
        """
        Comments just come from the global constant at the top.

        Polymorphic function:

            if not feedback_code:
                return possible feedback codes -> dict_keys
            if feedback_code:
                return feedback -> str
        """
        first_name = self.context["name"].split(' ')[0]
        comments = {
            'a': (
                f'{first_name}, awesome job breaking down topics into sub-topics.'
            ),
            'b': (
                f'Whoops! {first_name}, it looks like you submitted '
                'this blank. I\'m returning it without a grade; please '
                'resubmit ASAP!'
            ),
        }
        if not feedback_code:
            return comments.keys()
        return comments[feedback_code]


def user_select_assignment():
    assignment_name = input('Input assignment name ')
    classrooms = [
        'DeVries_Music_6_Curtis_Institute_of_Music',
        'DeVries_Music_5_Curtis_Institute_of_Music',
        'DeVries_Music_4_Curtis_Institute_of_Music',
        'Geltzeiler_HR_4B\n2020-2021'
    ]
    selections = set()
    inp = ''
    while inp != "d":
        for i, itm in enumerate(classrooms):
            print(f'{i}.\t{itm}')
        inp = input(
            'Select a classroom in which to grade that assignment or enter (d) for '
            'done.'
        )
        if inp.isdigit():
            idx = int(inp) - 1
            selections.add(classrooms[idx])
        print("***\n\tSelected classrooms:\n", '\n'.join(selections), '\n***')
    return assignment_name, list(selections)


def main(assignment, classrooms):
    atm = CustomAutomator(
        os.getenv('EMAIL_USERNAME'),
        os.getenv('EMAIL_PASSWORD_RAW'),
        assignment,
        classrooms
    )
    # MAIN ASSESSMENT LOOP
    for driver, context in atm:
        pass
    atm.driver.close()


if __name__ == '__main__':
    main('Writing- Creating Subtopics- 11/2', ['Geltzeiler_HR_4B\n2020-2021'])
