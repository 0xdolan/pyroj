"""
Julian day conversions aligned with KurdishDate (TypeScript) / Calendrical Calculations.

Date-only arithmetic uses the same numeric model as ``KurdishDate/src/dateConverter.ts``.
"""

from __future__ import annotations

import math
from datetime import date

# Epoch constants (same as KurdishDate dateConverter.ts)
GREGORIAN_EPOCH = 1721425.5
PERSIAN_EPOCH = 1948320.5
ISLAMIC_EPOCH = 1948439.5

# Kurdish solar year = Persian (Jalali) year + 1321 (same as legacy pyroj / Kurdipedia-style)
KURDISH_SOLAR_YEAR_OFFSET = 1321


def _mod(a: float | int, b: float | int) -> float:
    return float(a) - float(b) * math.floor(float(a) / float(b))


def is_gregorian_leap(year: int) -> bool:
    return (year % 4 == 0) and not ((year % 100 == 0) and (year % 400 != 0))


def gregorian_to_jdn(year: int, month: int, day: int) -> float:
    """Gregorian calendar date to Julian day number (same formula as KurdishDate)."""
    adj = 0 if month <= 2 else (-1 if is_gregorian_leap(year) else -2)
    return (
        (GREGORIAN_EPOCH - 1)
        + 365 * (year - 1)
        + math.floor((year - 1) / 4)
        + (-math.floor((year - 1) / 100))
        + math.floor((year - 1) / 400)
        + math.floor((367 * month - 362) / 12 + adj + day)
    )


def jdn_to_gregorian(jdn: float) -> tuple[int, int, int]:
    """Julian day number to Gregorian ``(year, month, day)`` with month 1..12."""
    wjd = math.floor(jdn - 0.5) + 0.5
    depoch = wjd - GREGORIAN_EPOCH
    quadricent = math.floor(depoch / 146097)
    dqc = _mod(depoch, 146097)
    cent = math.floor(dqc / 36524)
    dcent = _mod(dqc, 36524)
    quad = math.floor(dcent / 1461)
    dquad = _mod(dcent, 1461)
    yindex = math.floor(dquad / 365)
    year = int(quadricent * 400 + cent * 100 + quad * 4 + yindex)
    if not ((cent == 4) or (yindex == 4)):
        year += 1
    day_of_year = wjd - gregorian_to_jdn(year, 1, 1)
    if wjd < gregorian_to_jdn(year, 3, 1):
        leapadj = 0.0
    else:
        leapadj = 1.0 if is_gregorian_leap(year) else 2.0
    month = int(math.floor(((day_of_year + leapadj) * 12 + 373) / 367))
    day = int(wjd - gregorian_to_jdn(year, month, 1) + 1)
    return year, month, day


def is_persian_leap_year(year: int) -> bool:
    """Persian (Jalali) leap year (2820-year cycle), same rule as KurdishDate."""
    return ((((((year - (474 if year >= 0 else 473)) % 2820) + 474) + 38) * 682) % 2816) < 682


def persian_days_in_month(year: int, month: int) -> int:
    if month < 1 or month > 12:
        raise ValueError("month must be 1..12")
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if is_persian_leap_year(year) else 29


def persian_to_jdn(year: int, month: int, day: int) -> float:
    epbase = year - (474 if year >= 0 else 473)
    epyear = 474 + _mod(epbase, 2820)
    return (
        day
        + ((month - 1) * 31 if month <= 7 else ((month - 1) * 30 + 6))
        + math.floor((epyear * 682 - 110) / 2816)
        + (epyear - 1) * 365
        + math.floor(epbase / 2820) * 1029983
        + (PERSIAN_EPOCH - 1)
    )


def jdn_to_persian(jdn: float) -> tuple[int, int, int]:
    jdn = math.floor(jdn) + 0.5
    depoch = jdn - persian_to_jdn(475, 1, 1)
    cycle = math.floor(depoch / 1029983)
    cyear = _mod(depoch, 1029983)
    if cyear == 1029982:
        ycycle = 2820
    else:
        aux1 = math.floor(cyear / 366)
        aux2 = _mod(cyear, 366)
        ycycle = math.floor((2134 * aux1 + 2816 * aux2 + 2815) / 1028522) + aux1 + 1
    year = int(ycycle + 2820 * cycle + 474)
    if year <= 0:
        year -= 1
    day_of_year = jdn - persian_to_jdn(year, 1, 1) + 1
    if day_of_year <= 186:
        month = int(math.ceil(day_of_year / 31))
    else:
        month = int(math.ceil((day_of_year - 6) / 30))
    day = int(jdn - persian_to_jdn(year, month, 1) + 1)
    return year, month, day


def is_islamic_leap_year(year: int) -> bool:
    """Tabular Islamic leap year (11-year cycle), KurdishDate / Emacs-style."""
    return ((year * 11) + 14) % 30 < 11


def islamic_to_jdn(year: int, month: int, day: int) -> float:
    """Tabular Islamic date to JDN (same closed form as KurdishDate)."""
    return (
        day
        + math.ceil(29.5 * (month - 1))
        + (year - 1) * 354
        + math.floor((3 + 11 * year) / 30)
        + ISLAMIC_EPOCH
        - 1
    )


def jdn_to_islamic(jdn: float) -> tuple[int, int, int]:
    jdn = math.floor(jdn) + 0.5
    year = int(math.floor((30 * (jdn - ISLAMIC_EPOCH) + 10646) / 10631))
    month = min(
        12,
        int(math.ceil((jdn - (29 + islamic_to_jdn(year, 1, 1))) / 29.5) + 1),
    )
    day = int(jdn - islamic_to_jdn(year, month, 1) + 1)
    return year, month, day


def islamic_days_in_month(year: int, month: int) -> int:
    if month in (1, 3, 5, 7, 9, 11):
        return 30
    if month in (2, 4, 6, 8, 10):
        return 29
    return 30 if is_islamic_leap_year(year) else 29


def js_weekday_from_date(d: date) -> int:
    """JavaScript ``Date#getDay()`` convention: Sunday=0 .. Saturday=6."""
    return (d.weekday() + 1) % 7


def gregorian_weekday_to_persian_weekday(js_weekday: int) -> int:
    """
    Weekday index 1..7 used by KurdishDate for Persian/Kurdish (Saturday-first ordering
    in locale tables), derived from JS weekday.
    """
    if js_weekday + 2 == 8:
        return 1
    if js_weekday + 2 == 7:
        return 7
    return js_weekday + 2


def persian_weekday_from_gregorian(d: date) -> int:
    """1-based weekday compatible with KurdishDate ``day()`` for Kurdish/Persian calendar."""
    return gregorian_weekday_to_persian_weekday(js_weekday_from_date(d))
