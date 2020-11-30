import datetime
from persiantools.jdatetime import JalaliDate


class Rojjmer:

    """ Rojjmeri Kurdi"""

    # class variable
    leap_mod = [1, 5, 6, 9, 13, 17, 22, 30]
    ku_months = [
        [["خاکەلێوە", "نەورۆز"], ["بانەمەڕ", "گوڵان"], "جۆزەردان"],
        ["پووشپەڕ", "گەلاوێژ", "خەرمانان"],
        ["ڕەزبەر", ["گەڵاڕێزان", "خەزەڵوەر"], "سەرماوەز"],
        ["بەفرانبار", "ڕێبەندان", "ڕەشەمێ"],
    ]
    ku_month_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, [29, 30]]
    weekDays = (
        "شەممە",
        "یەکشەممە",
        "دووشەممە",
        "سێشەممە",
        "چوارشەممە",
        "پێنجشەممە",
        "هەینی",
    )

    # init method
    def __init__(
        self, year: int, month: int, day: int,
    ):

        """ init method """

        self.year = year
        self.month = month
        self.day = day
        self.whole_year = datetime.date(self.year, self.month, self.day)
        self.shamsi_year = JalaliDate(self.whole_year).year

    # Check if the Shamsi year is leap or not
    def is_leap(self) -> bool:

        """if Shamsi Year mod 33 return one of below numbers, it is leap year:
        [1, 5, 6, 9, 13, 17, 22, 30]
        """

        mod_number = 33
        if self.shamsi_year % mod_number in self.leap_mod:
            return True
        else:
            return False

    # Getting the Kurdish year
    def ku_year(self):

        """Getting the Kurdish year"""

        if self.shamsi_year == self.is_leap:
            kurdish_year = self.shamsi_year + 620 + 700
        else:
            kurdish_year = self.shamsi_year + 621 + 700
        return kurdish_year

    # Getting the Kurdish month
    def ku_month(self):

        """Getting the Kurdish month"""

        ku_month = JalaliDate(self.whole_year).month
        return ku_month

    # Getting the Kurdish day
    def ku_day(self):

        """Getting the Kurdish day"""

        ku_day = JalaliDate(self.whole_year).day
        return ku_day

    # Getting the Kurdish date
    def ku_date(self, solar=False):

        """Getting the Kurdish date"""

        if solar == False:
            tday = datetime.date(self.ku_year(), self.ku_month(), self.ku_day())
        elif solar == True:
            solar_year = self.year + 1321
            tday = datetime.date(solar_year, self.month, self.day)
        return tday

    # Kurdish WeekDays Names
    def hefte(self, abbr=False):

        """Kurdish WeekDays Names"""

        roj = self.whole_year
        if roj.weekday() == 5:
            if abbr == False:
                roji_hefte = self.weekDays[0]
            elif abbr == True:
                roji_hefte = self.weekDays[0][0]
        elif roj.weekday() == 6:
            if abbr == False:
                roji_hefte = self.weekDays[1]
            elif abbr == True:
                roji_hefte = self.weekDays[1][0]
        elif roj.weekday() == 0:
            if abbr == False:
                roji_hefte = self.weekDays[2]
            elif abbr == True:
                roji_hefte = self.weekDays[2][0]
        elif roj.weekday() == 1:
            if abbr == False:
                roji_hefte = self.weekDays[3]
            elif abbr == True:
                roji_hefte = self.weekDays[3][0]
        elif roj.weekday() == 2:
            if abbr == False:
                roji_hefte = self.weekDays[4]
            elif abbr == True:
                roji_hefte = self.weekDays[4][0]
        elif roj.weekday() == 3:
            if abbr == False:
                roji_hefte = self.weekDays[5]
            elif abbr == True:
                roji_hefte = self.weekDays[5][0]
        elif roj.weekday() == 4:
            if abbr == False:
                roji_hefte = self.weekDays[6]
            elif abbr == True:
                roji_hefte = self.weekDays[6][0]

        return roji_hefte

    # Kurdish Month Names
    def month_name(self, second_name=False):

        """ Kurdish Month Names"""

        if self.ku_month() == 1 and second_name == False:
            mang_name = self.ku_months[0][0][0]
        elif self.ku_month() == 1 and second_name == True:
            mang_name = self.ku_months[0][0][1]
        elif self.ku_month() == 2 and second_name == False:
            mang_name = self.ku_months[0][1][0]
        elif self.ku_month() == 2 and second_name == True:
            mang_name = self.ku_months[0][1][1]
        elif self.ku_month() == 3:
            mang_name = self.ku_months[0][2]
        elif self.ku_month() == 4:
            mang_name = self.ku_months[1][0]
        elif self.ku_month() == 5:
            mang_name = self.ku_months[1][1]
        elif self.ku_month() == 6:
            mang_name = self.ku_months[1][2]
        elif self.ku_month() == 7:
            mang_name = self.ku_months[2][0]
        elif self.ku_month() == 8 and second_name == False:
            mang_name = self.ku_months[2][1][0]
        elif self.ku_month() == 8 and second_name == True:
            mang_name = self.ku_months[2][1][1]
        elif self.ku_month() == 9:
            mang_name = self.ku_months[2][2]
        if self.ku_month() == 10:
            mang_name = self.ku_months[3][0]
        elif self.ku_month() == 11:
            mang_name = self.ku_months[3][1]
        elif self.ku_month() == 12:
            mang_name = self.ku_months[3][2]

        return mang_name
