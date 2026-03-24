"""Safe formatting (fixed tokens only)."""

from datetime import date

import pytest

from pyroj import (
    CalendarKind,
    KurdishDate,
    LocaleId,
    format_calendar_date,
    format_iso_date,
    get_locale,
    to_locale_digits,
    validate_pattern_safe,
)
from pyroj.exceptions import PyrojValueError


def test_format_iso_kurdish() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert format_iso_date(kd) == "2718-01-21"


def test_format_gregorian_calendar_english() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    s = format_calendar_date(
        kd,
        "%Y-%B-%d-%A",
        calendar=CalendarKind.GREGORIAN,
        locale=LocaleId.EN,
    )
    assert "2018" in s and "April" in s and "10" in s and "Tuesday" in s


def test_format_kurdish_ku_locale_month() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale=LocaleId.KU,
    )
    assert "خاک" in s


def test_locale_digits() -> None:
    loc = get_locale(LocaleId.FA)
    out = to_locale_digits("2718", loc)
    assert out == "۲۷۱۸"
    assert all(ord(ch) > 127 for ch in out)


def test_validate_pattern_rejects_braces() -> None:
    with pytest.raises(PyrojValueError):
        validate_pattern_safe("{YYYY}")


def test_format_rejects_braces() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    with pytest.raises(PyrojValueError):
        format_calendar_date(kd, "YYYY{MM}")


def test_literal_text_preserved() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert format_calendar_date(kd, "[[") == "[["


def test_pattern_length_limit() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    with pytest.raises(PyrojValueError):
        format_calendar_date(kd, "Y" * 600)
