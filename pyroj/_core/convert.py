"""
Julian day conversions aligned with KurdishDate (TypeScript) / Calendrical Calculations.

Date-only arithmetic uses the same numeric model as ``KurdishDate/src/dateConverter.ts``.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta

from pyroj.exceptions import PyrojRangeError, PyrojValueError

# Epoch constants (same as KurdishDate dateConverter.ts)
GREGORIAN_EPOCH = 1721425.5
PERSIAN_EPOCH = 1948320.5
ISLAMIC_EPOCH = 1948439.5
MIN_SUPPORTED_YEAR = 1
MAX_SUPPORTED_YEAR = 9999

# Kurdish solar year = Persian (Jalali) year + 1321 (same as legacy pyroj / Kurdipedia-style)
KURDISH_SOLAR_YEAR_OFFSET = 1321


def _mod(a: float | int, b: float | int) -> float:
    return float(a) - float(b) * math.floor(float(a) / float(b))


def _require_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise PyrojValueError(f"{name} must be int (bool is not allowed)")
    return value


def _require_finite_number(name: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PyrojValueError(f"{name} must be a finite number")
    out = float(value)
    if not math.isfinite(out):
        raise PyrojValueError(f"{name} must be finite")
    return out


def _require_year_bounds(name: str, year: int) -> int:
    if year < MIN_SUPPORTED_YEAR or year > MAX_SUPPORTED_YEAR:
        raise PyrojRangeError(
            f"{name} must be in [{MIN_SUPPORTED_YEAR}, {MAX_SUPPORTED_YEAR}], got {year}"
        )
    return year


def is_gregorian_leap(year: int) -> bool:
    year = _require_int("year", year)
    _require_year_bounds("year", year)
    return (year % 4 == 0) and not ((year % 100 == 0) and (year % 400 != 0))


def gregorian_to_jdn(year: int, month: int, day: int) -> float:
    """Gregorian calendar date to Julian day number (same formula as KurdishDate)."""
    year = _require_int("year", year)
    month = _require_int("month", month)
    day = _require_int("day", day)
    _require_year_bounds("year", year)
    try:
        date(year, month, day)
    except ValueError as exc:
        raise PyrojRangeError(str(exc)) from exc
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
    jdn = _require_finite_number("jdn", jdn)
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


def gregorian_datetime_to_jdn(dt: datetime) -> float:
    """Gregorian naive datetime to JDN, including fractional day."""
    if not isinstance(dt, datetime):
        raise PyrojValueError("dt must be datetime.datetime")
    base = gregorian_to_jdn(dt.year, dt.month, dt.day)
    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1_000_000
    return base + seconds / 86400


def jdn_to_gregorian_datetime(jdn: float) -> datetime:
    """JDN to Gregorian naive datetime (microsecond precision)."""
    jdn = _require_finite_number("jdn", jdn)
    y, m, d = jdn_to_gregorian(jdn)
    day_start = math.floor(jdn - 0.5) + 0.5
    frac = jdn - day_start
    total_microseconds = int(round(frac * 86_400_000_000))
    if total_microseconds >= 86_400_000_000:
        total_microseconds = 0
        base = datetime(y, m, d) + timedelta(days=1)
        return base
    seconds, microseconds = divmod(total_microseconds, 1_000_000)
    return datetime(y, m, d) + timedelta(seconds=seconds, microseconds=microseconds)


def is_persian_leap_year(year: int) -> bool:
    """Persian (Jalali) leap year (2820-year cycle), same rule as KurdishDate."""
    year = _require_int("year", year)
    _require_year_bounds("year", year)
    return ((((((year - (474 if year >= 0 else 473)) % 2820) + 474) + 38) * 682) % 2816) < 682


def persian_days_in_month(year: int, month: int) -> int:
    year = _require_int("year", year)
    month = _require_int("month", month)
    _require_year_bounds("year", year)
    if month < 1 or month > 12:
        raise PyrojRangeError("month must be 1..12")
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if is_persian_leap_year(year) else 29


def persian_to_jdn(year: int, month: int, day: int) -> float:
    year = _require_int("year", year)
    month = _require_int("month", month)
    day = _require_int("day", day)
    _require_year_bounds("year", year)
    dim = persian_days_in_month(year, month)
    if day < 1 or day > dim:
        raise PyrojRangeError(f"day must be 1..{dim} for Persian month {month}")
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
    jdn = _require_finite_number("jdn", jdn)
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
    year = _require_int("year", year)
    _require_year_bounds("year", year)
    return ((year * 11) + 14) % 30 < 11


def islamic_to_jdn(year: int, month: int, day: int) -> float:
    """Tabular Islamic date to JDN (same closed form as KurdishDate)."""
    year = _require_int("year", year)
    month = _require_int("month", month)
    day = _require_int("day", day)
    _require_year_bounds("year", year)
    dim = islamic_days_in_month(year, month)
    if day < 1 or day > dim:
        raise PyrojRangeError(f"day must be 1..{dim} for Islamic month {month}")
    return (
        day
        + math.ceil(29.5 * (month - 1))
        + (year - 1) * 354
        + math.floor((3 + 11 * year) / 30)
        + ISLAMIC_EPOCH
        - 1
    )


def jdn_to_islamic(jdn: float) -> tuple[int, int, int]:
    jdn = _require_finite_number("jdn", jdn)
    jdn = math.floor(jdn) + 0.5
    year = int(math.floor((30 * (jdn - ISLAMIC_EPOCH) + 10646) / 10631))
    month = min(
        12,
        int(math.ceil((jdn - (29 + islamic_to_jdn(year, 1, 1))) / 29.5) + 1),
    )
    day = int(jdn - islamic_to_jdn(year, month, 1) + 1)
    return year, month, day


def islamic_days_in_month(year: int, month: int) -> int:
    year = _require_int("year", year)
    month = _require_int("month", month)
    _require_year_bounds("year", year)
    if month < 1 or month > 12:
        raise PyrojRangeError("month must be 1..12")
    if month in (1, 3, 5, 7, 9, 11):
        return 30
    if month in (2, 4, 6, 8, 10):
        return 29
    return 30 if is_islamic_leap_year(year) else 29


def js_weekday_from_date(d: date) -> int:
    """JavaScript ``Date#getDay()`` convention: Sunday=0 .. Saturday=6."""
    if not isinstance(d, date):
        raise PyrojValueError("d must be datetime.date")
    return (d.weekday() + 1) % 7


def gregorian_weekday_to_persian_weekday(js_weekday: int) -> int:
    """
    Weekday index 1..7 used by KurdishDate for Persian/Kurdish (Saturday-first ordering
    in locale tables), derived from JS weekday.
    """
    js_weekday = _require_int("js_weekday", js_weekday)
    if js_weekday < 0 or js_weekday > 6:
        raise PyrojRangeError("js_weekday must be in 0..6")
    if js_weekday + 2 == 8:
        return 1
    if js_weekday + 2 == 7:
        return 7
    return js_weekday + 2


def persian_weekday_from_gregorian(d: date) -> int:
    """1-based weekday compatible with KurdishDate ``day()`` for Kurdish/Persian calendar."""
    return gregorian_weekday_to_persian_weekday(js_weekday_from_date(d))
