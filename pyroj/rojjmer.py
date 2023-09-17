# -*- coding: utf-8 -*-

import datetime
import io
import sys

import pytz
from kurdish_calendar import (
    calendarAbsoluteFromGregorian,
    calendarDayNumber,
    calendarDayOfWeek,
    calendarExtractMonth,
    calendarIslamicDayNumber,
    calendarIslamicDayOfWeek,
    calendarKurdishDayOfWeek,
    calendarKurdishDayOfWeekName,
    calendarKurdishFromGregorian,
    calendarKurdishFromIslamic,
    calendarKurdishFromPersian,
    calendarKurdishMonth,
    calendarKurdishToGregorian,
    calendarKurdishToIslamic,
    calendarKurdishToPersian,
    calendarPersianDayOfWeek,
)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")


class Rojjmer:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_datetime(self):
        return datetime.date(self.year, self.month, self.day)

    def kurdish_to_gregorian(self):
        # d = str(my_date).split("-")
        date = [self.month, self.day, self.year]
        month, day, year = calendarKurdishToGregorian(date)

        return datetime.date(year, month, day)

    def gregorian_to_kurdish(self):
        date = [self.month, self.day, self.year]
        month, day, year = calendarKurdishFromGregorian(date)

        return datetime.date(year, month, day)
