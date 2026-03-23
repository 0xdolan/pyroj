"""Static locale tables (Saturday-first for Kurdish/Persian/Islamic; Monday-first for Gregorian)."""

from __future__ import annotations

from pyroj.locales.types import CalendarNames, LocaleData, LocaleId

# --- English (Latin) ---
_EN_G = CalendarNames(
    months=(
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ),
    months_short=("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
    weekdays=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
    weekdays_short=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
    weekdays_min=("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"),
)
_EN_P = CalendarNames(
    months=(
        "Farvardin",
        "Ordibehesht",
        "Khordad",
        "Tir",
        "Mordad",
        "Shahrivar",
        "Mehr",
        "Aban",
        "Azar",
        "Dey",
        "Bahman",
        "Esfand",
    ),
    months_short=("Far", "Ord", "Kho", "Tir", "Mor", "Sha", "Meh", "Aba", "Aza", "Dey", "Bah", "Esf"),
    weekdays=(
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ),
    weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
    weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
)
_EN_K = CalendarNames(
    months=(
        "Xakelêw",
        "Gulan",
        "Cozerdan",
        "Pûşper",
        "Gelawêj",
        "Xermanan",
        "Rezber",
        "Gelarêzan",
        "Sermawez",
        "Befranbar",
        "Rêbendan",
        "Reşeme",
    ),
    months_short=(
        "Xak",
        "Gul",
        "Cozerd",
        "Pûşper",
        "Gelawêj",
        "Xerman",
        "Rezber",
        "Gelarêz",
        "Serma",
        "Befran",
        "Rêbend",
        "Reşeme",
    ),
    weekdays=_EN_P.weekdays,
    weekdays_short=_EN_P.weekdays_short,
    weekdays_min=_EN_P.weekdays_min,
)
_EN_I = CalendarNames(
    months=(
        "Muharram",
        "Safar",
        "Rabi' al-awwal",
        "Rabi' al-Thani",
        "Jumada al-awwal",
        "Jumada al-Thani",
        "Rajab",
        "Sha'ban",
        "Ramadan",
        "Shawwal",
        "Dhu al-Qi'dah",
        "Dhu al-Hijjah",
    ),
    months_short=("Muh", "Saf", "R-I", "R-II", "J-I", "J-II", "Raj", "Sha", "Ram", "Shaw", "ZQ", "ZH"),
    weekdays=_EN_P.weekdays,
    weekdays_short=_EN_P.weekdays_short,
    weekdays_min=_EN_P.weekdays_min,
)

# --- Kurdish (Kurmanji-style Arabic script, from KurdishDate ku.ts) ---
_KU_G_MONTHS = (
    "یەنایر",
    "فەبرایر",
    "مارس",
    "ئەپریل",
    "مایۆ",
    "یونیۆ",
    "یولیۆ",
    "ئۆغستەس",
    "سێپتەمبەر",
    "ئۆکتۆبەر",
    "نۆڤەمبەر",
    "دیسەمبەر",
)
_KU_G = CalendarNames(
    months=_KU_G_MONTHS,
    months_short=_KU_G_MONTHS,
    weekdays=("دووشەممە", "سێشەممە", "چوارشەممە", "پێنجشەممە", "هەینی", "شەممە", "یەکشەممە"),
    weekdays_short=("دوو", "سێ", "چوار", "پێنج", "هەینی", "شەممە", "یەک"),
    weekdays_min=("د", "س", "چ", "پ", "ه", "ش", "ی"),
)
_KU_P = CalendarNames(
    months=(
        "فەرڤەردین",
        "ئۆردیبێهێشت",
        "خۆرداد",
        "تیر",
        "مۆرداد",
        "شەهریڤەر",
        "مێهر",
        "ئابان",
        "ئازەر",
        "دێی",
        "بەهمەن",
        "ئێسفەند",
    ),
    months_short=("فەر", "ئۆرد", "خۆرد", "تیر", "مۆرد", "شەهر", "مێهر", "ئابا", "ئازەر", "دێی", "بەهم", "ئێسف"),
    weekdays=(
        "شەممە",
        "یەکشەممە",
        "دووشەممە",
        "سێشەممە",
        "چوارشەممە",
        "پێنجشەممە",
        "هەینی",
    ),
    weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
    weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
)
_KU_K = CalendarNames(
    months=(
        "خاکەڵێوە",
        "گوڵان",
        "جۆزەردان",
        "پووشپەڕ",
        "گەلاوێژ",
        "خەرمانان",
        "ڕەزبەر",
        "گەڵاڕێزان",
        "سەرماوەز",
        "بەفرانبار",
        "ڕێبەندان",
        "ڕەشەمێ",
    ),
    months_short=("خاک", "گوڵان", "جۆزەرد", "پووشپەڕ", "گەلاوێژ", "خەرمان", "ڕەزبەر", "گەڵاڕێز", "سەرما", "بەفران", "ڕێبەند", "ڕەشەمێ"),
    weekdays=_KU_P.weekdays,
    weekdays_short=_KU_P.weekdays_short,
    weekdays_min=_KU_P.weekdays_min,
)
_KU_I = CalendarNames(
    months=(
        "موحەڕڕەم",
        "سەفەر",
        "ڕەبیعەلئەووەل",
        "ڕەبیعەلئەسسانی",
        "جەمادەلئوولا",
        "جومادەلئاخیر",
        "ڕەجەب",
        "شەعبان",
        "ڕەمەزان",
        "شەووال",
        "زولقەعدە",
        "زولحەججە",
    ),
    months_short=("موح", "سەف", "ڕەبیع١", "ڕەبیع٢", "جەماد-١", "جەماد-٢", "ڕەج", "شەعب", "ڕەمەز", "شەو", "زولقەع", "زولحەج"),
    weekdays=_KU_P.weekdays,
    weekdays_short=_KU_P.weekdays_short,
    weekdays_min=_KU_P.weekdays_min,
)

# --- Persian (fa.ts) — Gregorian Monday-first; others Saturday-first ---
_FA_G = CalendarNames(
    months=(
        "ژانویه",
        "فوریه",
        "مارس",
        "آوریل",
        "مه",
        "ژوئن",
        "ژوئیه",
        "اوت",
        "سپتامبر",
        "اکتبر",
        "نوامبر",
        "دسامبر",
    ),
    months_short=("ژان", "فور", "مار", "آور", "مه", "ژوئ", "ژوی", "اوت", "سپت", "اکت", "نوا", "دسا"),
    weekdays=("دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "آدینه", "شنبه", "یک‌شنبه"),
    weekdays_short=("دو", "سه", "چهار", "پنج", "آد", "شنبه", "یک"),
    weekdays_min=("د", "س", "چ", "پ", "آ", "ش", "ی"),
)
_FA_P = CalendarNames(
    months=(
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ),
    months_short=("فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر", "دی", "بهم", "اسف"),
    weekdays=("شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "آدینه"),
    weekdays_short=("شنبه", "یک", "دو", "سه", "چهار", "پنج", "آد"),
    weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "آ"),
)
_FA_K = CalendarNames(
    months=(
        "خاکلیوٍَ",
        "گُلان",
        "جوز‌َردان",
        "پوشپَر",
        "گلاویژ",
        "خرمانان",
        "رَزبَر",
        "گلاریزان",
        "سرماوز",
        "بَفرانبار",
        "ریبندان",
        "رَشَمی",
    ),
    months_short=("خاک", "گل", "جوزرد", "پوشپَر", "گلاویژ", "خرمان", "رَزبَر", "گلاریز", "سرما", "بَفران", "ریبند", "رَشَمی"),
    weekdays=_FA_P.weekdays,
    weekdays_short=_FA_P.weekdays_short,
    weekdays_min=_FA_P.weekdays_min,
)
_FA_I = CalendarNames(
    months=(
        "محرم",
        "صفر",
        "ربیع‌الاول",
        "ربیع‌الثانی",
        "جمادی‌الاول",
        "جمادی‌الثانی",
        "رجب",
        "شعبان",
        "رمضان",
        "شوال",
        "ذیقعده",
        "ذیحجه",
    ),
    months_short=("محر", "صفر", "ربیع۱", "ربیع۲", "جمادی۱", "جمادی۲", "رجب", "شعب", "رمض", "شو", "ذیقع", "ذیحج"),
    weekdays=_FA_P.weekdays,
    weekdays_short=_FA_P.weekdays_short,
    weekdays_min=_FA_P.weekdays_min,
)

# --- Turkish (Gregorian/Islamic Turkish; Kurdish solar Latin) ---
_TR_G = CalendarNames(
    months=(
        "Ocak",
        "Şubat",
        "Mart",
        "Nisan",
        "Mayıs",
        "Haziran",
        "Temmuz",
        "Ağustos",
        "Eylül",
        "Ekim",
        "Kasım",
        "Aralık",
    ),
    months_short=("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"),
    weekdays=("Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"),
    weekdays_short=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"),
    weekdays_min=("Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"),
)
_TR_P = CalendarNames(
    months=_EN_P.months,
    months_short=_EN_P.months_short,
    weekdays=_EN_P.weekdays,
    weekdays_short=_EN_P.weekdays_short,
    weekdays_min=_EN_P.weekdays_min,
)
_TR_K = CalendarNames(
    months=_EN_K.months,
    months_short=_EN_K.months_short,
    weekdays=_EN_K.weekdays,
    weekdays_short=_EN_K.weekdays_short,
    weekdays_min=_EN_K.weekdays_min,
)
_TR_I = CalendarNames(
    months=(
        "Muharrem",
        "Safer",
        "Rebiülevvel",
        "Rebiülahir",
        "Cemaziyelevvel",
        "Cemaziyelahir",
        "Recep",
        "Şaban",
        "Ramazan",
        "Şevval",
        "Zilkade",
        "Zilhicce",
    ),
    months_short=("Muh", "Saf", "R-I", "R-II", "C-I", "C-II", "Rec", "Şab", "Ram", "Şev", "ZK", "ZH"),
    weekdays=_EN_I.weekdays,
    weekdays_short=_EN_I.weekdays_short,
    weekdays_min=_EN_I.weekdays_min,
)

# --- Arabic (MSA-style Gregorian; Islamic Arabic; Kurdish/Persian Arabic script) ---
_AR_G_MONTHS = (
    "يناير",
    "فبراير",
    "مارس",
    "أبريل",
    "مايو",
    "يونيو",
    "يوليو",
    "أغسطس",
    "سبتمبر",
    "أكتوبر",
    "نوفمبر",
    "ديسمبر",
)
_AR_G = CalendarNames(
    months=_AR_G_MONTHS,
    months_short=_AR_G_MONTHS,
    weekdays=("الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"),
    weekdays_short=("إثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت", "أحد"),
    weekdays_min=("ن", "ث", "ر", "خ", "ج", "س", "ح"),
)
_AR_P = CalendarNames(
    months=(
        "فروردين",
        "أرديبهشت",
        "خرداد",
        "تير",
        "مرداد",
        "شهريور",
        "مهر",
        "آبان",
        "آذر",
        "دي",
        "بهمن",
        "اسفند",
    ),
    months_short=("فر", "أرد", "خر", "تير", "مر", "شه", "مه", "آب", "آذ", "دي", "به", "اس"),
    weekdays=("السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"),
    weekdays_short=("سبت", "أحد", "إثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة"),
    weekdays_min=("س", "ح", "ث", "ث", "ر", "خ", "ج"),
)
_AR_K = CalendarNames(
    months=(
        "خاكه‌لوه",
        "گولان",
        "جوزه‌ردان",
        "بوشپه‌ر",
        "گه‌لاويج",
        "خرمانان",
        "ره‌زبه‌ر",
        "گه‌لاريزان",
        "سرماوه‌ز",
        "به‌فرانبار",
        "ريبه‌ندان",
        "ره‌شه‌مه",
    ),
    months_short=("خاك", "گل", "جوز", "بوش", "گه‌ل", "خر", "ره‌ز", "گه‌ل", "سر", "به‌ف", "ريب", "ره‌ش"),
    weekdays=_AR_P.weekdays,
    weekdays_short=_AR_P.weekdays_short,
    weekdays_min=_AR_P.weekdays_min,
)
_AR_I = CalendarNames(
    months=(
        "محرم",
        "صفر",
        "ربيع الأول",
        "ربيع الآخر",
        "جمادى الأولى",
        "جمادى الآخر",
        "رجب",
        "شعبان",
        "رمضان",
        "شوال",
        "ذو القعدة",
        "ذو الحجة",
    ),
    months_short=("مح", "صف", "ر1", "ر2", "ج1", "ج2", "رج", "شع", "رم", "شو", "قع", "حج"),
    weekdays=_AR_P.weekdays,
    weekdays_short=_AR_P.weekdays_short,
    weekdays_min=_AR_P.weekdays_min,
)

_DIGITS_EN = tuple(str(i) for i in range(10))
_DIGITS_FA = ("۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹")
_DIGITS_AR = ("٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩")

LOCALE_EN = LocaleData(
    locale_id=LocaleId.EN,
    gregorian=_EN_G,
    persian=_EN_P,
    kurdish=_EN_K,
    islamic=_EN_I,
    digits=_DIGITS_EN,
    am_pm=("am", "pm"),
)

LOCALE_KU = LocaleData(
    locale_id=LocaleId.KU,
    gregorian=_KU_G,
    persian=_KU_P,
    kurdish=_KU_K,
    islamic=_KU_I,
    digits=_DIGITS_AR,
    am_pm=("ب.ن", "د.ن"),
)

LOCALE_FA = LocaleData(
    locale_id=LocaleId.FA,
    gregorian=_FA_G,
    persian=_FA_P,
    kurdish=_FA_K,
    islamic=_FA_I,
    digits=_DIGITS_FA,
    am_pm=("ق.ظ", "ب.ظ"),
)

LOCALE_TR = LocaleData(
    locale_id=LocaleId.TR,
    gregorian=_TR_G,
    persian=_TR_P,
    kurdish=_TR_K,
    islamic=_TR_I,
    digits=_DIGITS_EN,
    am_pm=("öö", "ös"),
)

LOCALE_AR = LocaleData(
    locale_id=LocaleId.AR,
    gregorian=_AR_G,
    persian=_AR_P,
    kurdish=_AR_K,
    islamic=_AR_I,
    digits=_DIGITS_AR,
    am_pm=("ص", "م"),
)

LOCALE_BY_ID: dict[LocaleId, LocaleData] = {
    LocaleId.EN: LOCALE_EN,
    LocaleId.KU: LOCALE_KU,
    LocaleId.FA: LOCALE_FA,
    LocaleId.TR: LOCALE_TR,
    LocaleId.AR: LOCALE_AR,
}


def get_locale(locale_id: LocaleId) -> LocaleData:
    """Return the static :class:`LocaleData` for ``locale_id``."""
    return LOCALE_BY_ID[locale_id]
