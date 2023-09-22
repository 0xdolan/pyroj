# -*- coding: utf-8 -*-

from math import floor


class Utils:
    """Utils class for Kurdish Calendar (Rojjmer)"""

    def __init__(self):
        """init method for Utils class"""

    def div(self, x, y):
        return floor(x / y)

    def mod(self, x, y):
        r = x % y
        return r + y if y * r < 0 else r


class Rojjmer(Utils):
    def __init__(self, year, month, day):
        """init method for Rojjmer class"""
        self.year = year
        self.month = month
        self.day = day

        if self.year == 0:
            raise ValueError("Year 0 does not exist in Kurdish Calendar")

        if self.year < 0:
            raise ValueError("Year cannot be negative")

        if self.month < 1 or self.month > 12:
            raise ValueError("Month should be between 1 and 12")

        if self.day < 1 or self.day > 31:
            raise ValueError("Day should be between 1 and 31")

    def is_leap(self):
        """check if the year is leap or not"""
        return self.mod(self.year, 4) == 0

    def is_persian_leap_year(self):
        """return persian leap year"""

        year = self.year

        if (
            year % 33 == 1
            or year % 33 == 5
            or year % 33 == 9
            or year % 33 == 13
            or year % 33 == 17
            or year % 33 == 22
            or year % 33 == 26
            or year % 33 == 30
        ):
            return True
        else:
            return False

    def is_islamic_leap_year(self):
        """check if the year is leap or not"""
        return self.mod(self.year, 30) == 2

    def get_day_numbers(self):
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]

        if self.is_leap():
            days_in_month[2] = 29

        day_of_year = self.day + sum(days_in_month[: self.month])
        return day_of_year

    def get_weeks_number(self):
        """return week number"""
        return self.div(self.get_day_numbers(), 7) + 1

    def get_day_of_week(self):
        """return day of week"""
        return self.mod(self.gregorian_to_absolute(), 7)

    def get_day_of_month(self):
        """return day of month"""
        return self.day

    def get_days_of_year(self):
        """return number of days in a year"""
        return 366 if self.is_leap() else 365

    def get_last_day_of_month(self):
        """return last day of month"""
        if self.month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif self.month in [4, 6, 9, 11]:
            return 30
        elif self.month == 2:
            return 29 if self.is_leap() else 28

    def get_persian_last_day_of_month(self):
        """return last day of month"""
        if self.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return 30
        elif self.month in [11, 12]:
            return 29 if self.is_persian_leap_year() else 28

    def get_islamic_last_day_of_month(self):
        """return last day of month"""
        if self.month in [1, 3, 5, 7, 9, 11]:
            return 30
        elif self.month in [2, 4, 6, 8, 10, 12]:
            return 29
        elif self.month == 13:
            return 30 if self.is_islamic_leap_year() else 29

    def gregorian_to_absolute(self):
        """return absolute date from gregorian date"""

        return (
            365 * (self.year - 1)
            + self.div(self.year - 1, 4)
            - self.div(self.year - 1, 100)
            + self.div(self.year - 1, 400)
            + self.get_day_numbers()
        )

    def absolute_to_gregorian(self):
        """return gregorian date from absolute date"""

        date = self.gregorian_to_absolute()

        # Constants for various time periods in days
        DAYS_PER_400_YEARS = 146097
        DAYS_PER_100_YEARS = 36524
        DAYS_PER_4_YEARS = 1461
        DAYS_PER_YEAR = 365

        # Calculate the number of cycles for each time period
        n400, date = divmod(date - 1, DAYS_PER_400_YEARS)
        n100, date = divmod(date, DAYS_PER_100_YEARS)
        n4, date = divmod(date, DAYS_PER_4_YEARS)
        n1, day = divmod(date, DAYS_PER_YEAR)

        # Calculate the year
        year = 400 * n400 + 100 * n100 + 4 * n4 + n1

        # Initialize month to 1
        month = 1

        # Check for leap years
        if n100 == 4 or n1 == 4:
            return [12, 31, year]

        year += 1

        # Find the month and day using a list of days in each month
        days_in_month = [
            0,
            31,
            28 if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0) else 29,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]

        while day > days_in_month[month]:
            day -= days_in_month[month]
            month += 1

        # add 1 to day to make it 1-based instead of 0-based
        day += 1

        return year, month, day

    def julian_to_absolute(self):
        """return absolute date from julian date"""

        year = int(self.year)
        month = int(self.month)

        absolute_date = (
            self.day
            + (
                1
                if (year % 100 == 0) and (not (year % 400 == 0)) and (month > 2)
                else 0
            )  # Leap year adjustment
            + (365 * (year - 1))  # Days in previous years
            + self.div((year - 1), 4)  # Leap year days
            - 2  # Adjustment factor
        )

        return absolute_date

    def get_persian_epoch(self):
        """return persian epoch"""
        year = 622
        month = 3
        day = 19

        return Rojjmer(year, month, day).gregorian_to_absolute()

    def get_islamic_epoch(self):
        """return islamic epoch"""
        year = 622
        month = 7
        day = 16

        return Rojjmer(year, month, day).gregorian_to_absolute()

    def persian_to_absolute(self):
        """return absolute date from persian date"""

        year = int(self.year)
        month = int(self.month)
        day = int(self.day)

        absolute_date = (
            day
            + (
                1
                if (year % 33 == 1)
                or (year % 33 == 5)
                or (year % 33 == 9)
                or (year % 33 == 13)
                or (year % 33 == 17)
                or (year % 33 == 22)
                or (year % 33 == 26)
                or (year % 33 == 30)
                and (month > 1)
                else 0
            )  # Leap year adjustment
            + (365 * (year - 1))  # Days in previous years
            + self.div((year - 1), 4)  # Leap year days
            - 2  # Adjustment factor
        )

        return absolute_date

    def get_perisan_year_from_absolute(self):
        """return persian year from absolute date"""

        absolute_date = self.gregorian_to_absolute()

        return self.div(absolute_date - self.get_persian_epoch(), 365)

    def absolute_to_persian(self):
        """Return Persian date from absolute date"""

        absolute_date = self.gregorian_to_absolute()
        persian_epoch = self.get_persian_epoch()

        days_difference = absolute_date - persian_epoch
        persian_year = self.get_perisan_year_from_absolute()

        # Calculate the day, month, and day of the week
        day = days_difference % 365
        if day == 0:
            day = 365
        month = 1
        while day > self.get_persian_last_day_of_month():
            day -= self.get_persian_last_day_of_month()
            month += 1

        # Return the Persian date as a tuple (year, month, day)
        return persian_year, month, day

    def islamic_to_absolute(self):
        """return absolute date from islamic date"""

        year = int(self.year)
        month = int(self.month)
        day = int(self.day)

        absolute_date = (
            day
            + (1 if (year % 30 == 2) and (month > 1) else 0)  # Leap year adjustment
            + (354 * (year - 1))  # Days in previous years
            + self.div((year - 1), 30)  # Leap year days
            - 2  # Adjustment factor
        )

        return absolute_date

    def absolute_to_islamic(self):
        """Return Islamic date from absolute date"""

        absolute_date = self.gregorian_to_absolute()
        islamic_epoch = self.get_islamic_epoch()

        days_difference = absolute_date - islamic_epoch
        islamic_year = self.div(days_difference, 354)

        # Calculate the day, month, and day of the week
        day = days_difference % 354
        if day == 0:
            day = 354
        month = 1
        while day > self.get_islamic_last_day_of_month():
            day -= self.get_islamic_last_day_of_month()
            month += 1

        # Return the Islamic date as a tuple (year, month, day)
        return islamic_year, month, day

    def persian_to_kurdish(self):
        year = int(self.year) + 1321

        return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    def kurdish_to_persian(self):
        year = int(self.year) - 1321
        return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    def kurdish_to_gregorian(self):
        """return gregorian date from kurdish date"""

        year = int(self.year) - 700
        return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    def kurdish_to_islamic(self):
        """return islamic date from kurdish date"""
        pass

    def islamic_to_kurdish(self):
        """return kurdish date from islamic date"""
        pass
