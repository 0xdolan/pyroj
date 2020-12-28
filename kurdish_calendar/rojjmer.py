import datetime
from persiantools.jdatetime import JalaliDate


class Rojjmer:

    """ Rojjmeri Kurdi"""

    # class variable
    leap_mod = [1, 5, 6, 9, 13, 17, 22, 30]
    ku_month = [
        [["خاکەلێوە", "نەورۆز"], ["بانەمەڕ", "گوڵان"], "جۆزەردان"],
        ["پووشپەڕ", "گەلاوێژ", "خەرمانان"],
        ["ڕەزبەر", ["گەڵاڕێزان", "خەزەڵوەر"], "سەرماوەز"],
        ["بەفرانبار", "ڕێبەندان", "ڕەشەمێ"],
    ]
    ku_month_latin = [
        [["Xakelêwe", "Newroz"], ["Banemeŕ", "Guĺan"], "Cozerdan"],
        ["Pûşpeŕ", "Gelawêj", "Xermanan"],
        ["Ŕezber", ["Geĺaŕêzan", "Xezeĺwer"], "Sermawez"],
        ["Befranbar", "Ŕêbendan", "Ŕeşemê"],
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

    weekDays_latin = (
        "Şemme",
        "Yekşemme",
        "Dûşemme",
        "Sêşemme",
        "Çwarşemme",
        "Pêncşemme",
        "Heynî",
    )

    # init method
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
    ):

        """ init method """

        self.year = year
        self.month = month
        self.day = day
        self.whole_year = datetime.date(self.year, self.month, self.day)
        self.shamsi_date = JalaliDate(self.whole_year)

    # Check if the Shamsi year is leap or not
    def is_leap(self, solar=False) -> bool:

        """if Shamsi Year mod 33 return one of below numbers, it is leap year:
        [1, 5, 6, 9, 13, 17, 22, 30]
        """
        # if solar == False:
        #     if self.year % 400 == 0:
        #         result = True
        #     if self.year % 100 == 0:
        #         result = False
        #     if self.year % 4 == 0:
        #         result = True
        #     else:
        #         result = False
        # elif solar == True:
        mod_number = 33
        if self.shamsi_date.year % mod_number in self.leap_mod:
            result = True
        else:
            result = False
        return result

    # Convert Gregorian and Solar date the Kurdish date
    def to_kurdish(self, whole_year, solar=False):

        """Convert Gregorian and Solar date the Kurdish date"""

        if solar == False:
            ku_date = self.whole_year
        elif solar == True:
            kurdish_year = self.shamsi_date.year + 1321
            # if self.whole_year.year == self.is_leap:
            #     # kurdish_year = self.whole_year.year + 620 + 700
            # else:
            #     kurdish_year = self.whole_year.year + 621 + 700
            ku_date = JalaliDate(
                kurdish_year, self.whole_year.month, self.whole_year.day
            )

        return ku_date

    # # Getting the Kurdish year
    # def ku_year(self):

    #     """Getting the Kurdish year"""

    #     if self.shamsi_year == self.is_leap:
    #         kurdish_year = self.shamsi_year + 620 + 700
    #     else:
    #         kurdish_year = self.shamsi_year + 621 + 700
    #     return kurdish_year

    # Convert Kurdish date to Gregorian date
    def to_gregorian(self, whole_year):

        """Convert Kurdish date to Gregorian date"""

        da = ""

        return da

    # Kurdish WeekDays Names
    def hefte(self, abbr=False, latin=False):

        """Kurdish WeekDays Names"""

        roj = self.whole_year
        if roj.weekday() == 5:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[0]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[0][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[0]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[0][0]
        elif roj.weekday() == 6:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[1]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[1][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[1]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[1][0]
        elif roj.weekday() == 0:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[2]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[2][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[2]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[2][0]
        elif roj.weekday() == 1:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[3]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[3][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[3]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[3][0]
        elif roj.weekday() == 2:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[4]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[4][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[4]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[4][0]
        elif roj.weekday() == 3:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[5]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[5][0]
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[5]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[5][0]
        elif roj.weekday() == 4:
            if abbr == False and latin == False:
                roji_hefte = self.weekDays[6]
            elif abbr == True and latin == False:
                roji_hefte = self.weekDays[6][0] + "ـ"
            elif abbr == False and latin == True:
                roji_hefte = self.weekDays_latin[6]
            elif abbr == True and latin == True:
                roji_hefte = self.weekDays_latin[6][0]
        return roji_hefte

    # Kurdish Month Names
    def month_name(self, second_name=False, latin=False):

        """ Kurdish Month Names"""

        mang = JalaliDate(self.whole_year).month

        if mang == 1 and second_name == False and latin == False:
            mang_name = self.ku_month[0][0][0]
        elif mang == 1 and second_name == True and latin == False:
            mang_name = self.ku_month[0][0][1]
        elif mang == 1 and second_name == False and latin == True:
            mang_name = self.ku_month_latin[0][0][0]
        if mang == 1 and second_name == True and latin == True:
            mang_name = self.ku_month_latin[0][0][1]
        elif mang == 2 and second_name == False and latin == False:
            mang_name = self.ku_month[0][1][0]
        elif mang == 2 and second_name == True and latin == False:
            mang_name = self.ku_month[0][1][1]
        elif mang == 2 and second_name == False and latin == True:
            mang_name = self.ku_month_latin[0][1][0]
        elif mang == 2 and second_name == True and latin == True:
            mang_name = self.ku_month_latin[0][1][1]
        elif mang == 3:
            mang_name = self.ku_month[0][2]
        elif mang == 4:
            mang_name = self.ku_month[1][0]
        elif mang == 5:
            mang_name = self.ku_month[1][1]
        elif mang == 6:
            mang_name = self.ku_month[1][2]
        elif mang == 7:
            mang_name = self.ku_month[2][0]
        elif mang == 8 and second_name == False and latin == False:
            mang_name = self.ku_month[2][1][0]
        elif mang == 8 and second_name == True and latin == False:
            mang_name = self.ku_month[2][1][1]
        elif mang == 8 and second_name == False and latin == True:
            mang_name = self.ku_month_latin[2][1][0]
        elif mang == 8 and second_name == True and latin == True:
            mang_name = self.ku_month_latin[2][1][1]
        elif mang == 9:
            mang_name = self.ku_month[2][2]
        elif mang == 10:
            mang_name = self.ku_month[3][0]
        elif mang == 11:
            mang_name = self.ku_month[3][1]
        elif mang == 12:
            mang_name = self.ku_month[3][2]

        return mang_name
