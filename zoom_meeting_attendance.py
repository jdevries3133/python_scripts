"""
Parse zoom attendance reports with teacherHelper
"""
from pathlib import Path

from teacherHelper import MeetingSet

meetings = MeetingSet(
    Path(
        '/'
        'Users',
        'JohnDeVries',
        'repos',
        'teacher_helper',
        'data',
        'zoom_attendance_reports'
    )
)
meetings.process()
breakpoint()
