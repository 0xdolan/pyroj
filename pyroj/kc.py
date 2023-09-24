# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from math import floor


class Rojjmer:
    """
    Kurdish Calendar (Rojjmer) class
    """

    # Persian calendar constants
    PERSIAN_EPOCH = datetime(622, 3, 21)  # March 21, 622 AD in the Gregorian calendar
    PERSIAN_DAYS_IN_YEAR = 365
    PERSIAN_DAYS_IN_LEAP_YEAR = 366
    PERSIAN_MONTH_LENGTHS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

    # Islamic calendar constants
    ISLAMIC_EPOCH = datetime(622, 7, 16)  # July 16, 622 AD in the Gregorian calendar
    ISLAMIC_DAYS_IN_YEAR = 354
    ISLAMIC_DAYS_IN_LEAP_YEAR = 355

    # JULIAN_DAY_NUMBER = 1721423.5

    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        """
        Initializer for Rojjmer class
        """

        # Validate the year
        if year == 0:
            raise ValueError("Year 0 does not exist in the Kurdish Calendar")
        if year < 0:
            raise ValueError("Year cannot be negative")

        # Validate the month
        if month < 1 or month > 12:
            raise ValueError("Month should be between 1 and 12")

        # Validate the day
        if day < 1 or day > 31:
            raise ValueError("Day should be between 1 and 31")

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def is_leap_year(self):
        """
        Check if a year is a leap year.
        """
        if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):
            return True
        return False

    def is_persian_leap_year(self):
        """
        Check if the year is a Persian leap year
        """
        year = self.year
        leap_year_remainders = [1, 5, 9, 13, 17, 22, 26, 30]

        return year % 33 in leap_year_remainders

    def is_islamic_leap_year(self):
        """Check if the current Islamic year is a leap year"""
        return (self.year * 11 + 14) % 30 < 11

    def get_day_of_year(self):
        """
        Get the day of the year
        """
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]

        if self.is_leap_year():
            days_in_month[2] = 29

        day_of_year = self.day + sum(days_in_month[: self.month])
        return day_of_year

    def get_islamic_month_lengths(self):
        """
        Get the lengths of Islamic months for a non-leap year
        """
        return [30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30]

    def get_weeks_number(self):
        """
        return week number
        """
        return floor(self.get_day_of_year() / 7)

    def get_day_of_week(self):
        """
        return day of week
        """
        return (self.gregorian_to_absolute() + 1) % 7

    def get_days_of_year(self):
        """
        return number of days in a year
        """
        return 366 if self.is_leap_year() else 365

    def get_days_of_month(self):
        """
        return number of days in a month
        """
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30]
        if self.is_leap_year():
            days_in_month[2] = 29

        return days_in_month[self.month]

    def get_last_day_of_month(self):
        """
        return last day of month
        """
        if self.month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif self.month in [4, 6, 9, 11]:
            return 30
        elif self.month == 2:
            return 29 if self.is_leap_year() else 28

    def get_persian_last_day_of_month(self):
        """
        return last day of month
        """
        if self.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return 30
        elif self.month in [11, 12]:
            return 29 if self.is_persian_leap_year() else 28

    def get_islamic_last_day_of_month(self):
        """
        return last day of month
        """
        if self.month in [1, 3, 5, 7, 9, 11]:
            return 30
        elif self.month in [2, 4, 6, 8, 10, 12]:
            return 29
        elif self.month == 13:
            return 30 if self.is_islamic_leap_year() else 29

    def gregorian_to_absolute(self):
        """
        return absolute date from gregorian date
        """
        gregorian_date = datetime(self.year, self.month, self.day)
        reference_date = datetime(1, 1, 1)  # January 1, 1 AD in the Gregorian calendar
        delta = gregorian_date - reference_date
        return delta.days

    def absolute_to_gregorian(self):
        """
        Return Gregorian date and time from absolute date
        """

        date = self.gregorian_to_absolute()
        time_delta = timedelta(days=date)
        return datetime(1, 1, 1) + time_delta

    # def julian_to_absolute(self):
    #     """
    #     Convert Julian date to absolute date
    #     """
    #     julian_date = self.gregorian_to_absolute() + self.JULIAN_DAY_NUMBER
    #     time_delta = timedelta(days=julian_date)
    #     return datetime(1, 1, 1) + time_delta

    def get_islamic_year_length(self, year):
        """Get the length of an Islamic year"""
        return (
            self.ISLAMIC_DAYS_IN_LEAP_YEAR
            if self.is_islamic_leap_year(year)
            else self.ISLAMIC_DAYS_IN_YEAR
        )

    def persian_to_absolute(self):
        """Convert Persian (Jalali) date to absolute date"""

        # Calculate the number of years, months, and days from the Persian epoch
        persian_year = self.year
        persian_month = self.month
        persian_day = self.day

        # Calculate days from years
        days_from_years = (persian_year - 1) * self.PERSIAN_DAYS_IN_YEAR

        # Calculate days from months
        days_from_months = sum(self.PERSIAN_MONTH_LENGTHS[: persian_month - 1])

        # Adjust for leap years
        leap_year_count = sum(
            1 for self.year in range(1, persian_year) if self.is_persian_leap_year()
        )
        days_from_months += leap_year_count

        # Calculate the total number of days
        total_days = days_from_years + days_from_months + persian_day

        # Calculate the absolute date from the Persian epoch
        persian_epoch = self.PERSIAN_EPOCH
        absolute_date = persian_epoch + timedelta(
            days=total_days - 1
        )  # Subtract 1 day to adjust for the epoch day

        return absolute_date

    def absolute_to_persian(self):
        """
        Convert an absolute date to a Persian (Jalali) date
        """

        absolute_date = self.gregorian_to_absolute()

        # Calculate the days difference between the absolute date and the Persian epoch
        delta = absolute_date - self.PERSIAN_EPOCH

        # Extract the number of days from the timedelta
        days_difference = delta.days

        # Initialize variables for Persian year, month, and day
        persian_year = self.get_persian_year_from_absolute(absolute_date)
        persian_month = 1
        persian_day = 1

        # Check if it's a leap year and set the month lengths accordingly
        if self.is_persian_leap_year():
            persian_month_lengths = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        else:
            persian_month_lengths = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30]

        # Subtract days for each month to find the Persian month and day
        for month_length in persian_month_lengths:
            if days_difference >= month_length:
                persian_month += 1
                days_difference -= month_length
            else:
                persian_day += days_difference
                break

        return persian_year, persian_month, persian_day

    def islamic_to_absolute(self):
        """
        Convert Islamic (Hijri) date to absolute date
        """

        # Constants for Islamic calendar calculations
        ISLAMIC_DAYS_IN_YEAR = 354
        ISLAMIC_DAYS_IN_LEAP_YEAR = 355

        # Calculate the days difference between the Islamic date and the Persian epoch
        days_difference = (self.year - 1) * ISLAMIC_DAYS_IN_YEAR

        # Adjust for leap years
        for i in range(1, self.year):
            if self.is_islamic_leap_year(i):
                days_difference += 1

        # Add days for each month
        days_difference += sum(self.get_islamic_month_lengths()[: self.month - 1])
        days_difference += self.day

        # Calculate the absolute date from the Persian epoch
        islamic_epoch = self.PERSIAN_EPOCH
        absolute_date = islamic_epoch + timedelta(
            days=days_difference,
            hours=self.hour,
            minutes=self.minute,
            seconds=self.second,
        )

        return absolute_date

    def absolute_to_islamic(self, absolute_date):
        """Convert an absolute date to an Islamic (Hijri) date"""

        # Calculate the days difference between the absolute date and the Persian epoch
        days_difference = (absolute_date - self.PERSIAN_EPOCH).days

        # Initialize variables for Islamic year, month, and day
        islamic_year = 1
        islamic_month = 1
        islamic_day = 1

        # Adjust for leap years
        while days_difference >= self.get_islamic_year_length(islamic_year):
            if self.is_islamic_leap_year(islamic_year):
                days_difference -= 1
            days_difference -= self.get_islamic_year_length(islamic_year)
            islamic_year += 1

        # Adjust for months and days
        while islamic_month <= 12 and days_difference >= self.get_islamic_month_length(
            islamic_year, islamic_month
        ):
            days_difference -= self.get_islamic_month_length(
                islamic_year, islamic_month
            )
            islamic_month += 1

        islamic_day += days_difference

        return islamic_year, islamic_month, islamic_day

    # def absolute_to_kurdish(self, absolute_date):
    #     """Convert an absolute date to a Kurdish date"""

    #     # Calculate the days difference between the absolute date and the Kurdish epoch
    #     days_difference = (absolute_date - self.KURDISH_EPOCH).days

    #     # Calculate Kurdish year, month, and day
    #     kurdish_year = 1
    #     kurdish_month = 1
    #     kurdish_day = 1

    #     # Adjust for leap years and months
    #     while days_difference >= self.get_kurdish_year_length(kurdish_year):
    #         days_difference -= self.get_kurdish_year_length(kurdish_year)
    #         kurdish_year += 1

    #     while kurdish_month <= 12 and days_difference >= self.get_kurdish_month_length(kurdish_year, kurdish_month):
    #         days_difference -= self.get_kurdish_month_length(kurdish_year, kurdish_month)
    #         kurdish_month += 1

    #     kurdish_day += days_difference

    #     return kurdish_year, kurdish_month, kurdish_day

    # def persian_to_kurdish(self):
    #     year = int(self.year) + 1321

    #     return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    # def kurdish_to_persian(self):
    #     year = int(self.year) - 1321
    #     return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    # def kurdish_to_gregorian(self):
    #     """return gregorian date from kurdish date"""

    #     year = int(self.year) - 700
    #     return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    # def gregorian_to_kurdish(self):
    #     """return kurdish date from gregorian date"""

    #     year = int(self.year) + 700
    #     return Rojjmer(year, self.month, self.day).absolute_to_gregorian()

    # def kurdish_to_islamic(self):
    #     """return islamic date from kurdish date"""
    #     pass

    # def islamic_to_kurdish(self):
    #     """return kurdish date from islamic date"""
    #     pass
