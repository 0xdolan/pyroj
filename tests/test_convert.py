"""Golden values aligned with KurdishDate (TypeScript) for 2018-04-10."""

from datetime import date, datetime

import pytest

from pyroj._core.convert import (
    gregorian_datetime_to_jdn,
    gregorian_to_jdn,
    gregorian_weekday_to_persian_weekday,
    islamic_to_jdn,
    jdn_to_gregorian,
    jdn_to_gregorian_datetime,
    jdn_to_islamic,
    jdn_to_persian,
    js_weekday_from_date,
    persian_to_jdn,
    persian_weekday_from_gregorian,
)
from pyroj.exceptions import PyrojRangeError, PyrojValueError


def test_gregorian_round_trip() -> None:
    d = date(2018, 4, 10)
    j = gregorian_to_jdn(d.year, d.month, d.day)
    assert jdn_to_gregorian(j) == (2018, 4, 10)


def test_kurdish_date_golden_april_10_2018() -> None:
    d = date(2018, 4, 10)
    j = gregorian_to_jdn(d.year, d.month, d.day)
    assert jdn_to_persian(j) == (1397, 1, 21)
    assert jdn_to_islamic(j) == (1439, 7, 24)
    assert 1397 + 1321 == 2718
    assert persian_weekday_from_gregorian(d) == 4
    assert js_weekday_from_date(d) == 2  # Tuesday in JS
    assert gregorian_weekday_to_persian_weekday(2) == 4


def test_persian_round_trip() -> None:
    y, m, d = 1397, 1, 21
    j = persian_to_jdn(y, m, d)
    assert jdn_to_persian(j) == (y, m, d)


def test_islamic_round_trip() -> None:
    y, m, d = 1439, 7, 24
    j = islamic_to_jdn(y, m, d)
    assert jdn_to_islamic(j) == (y, m, d)


def test_convert_rejects_bool_and_ranges() -> None:
    with pytest.raises(PyrojValueError):
        gregorian_to_jdn(True, 1, 1)  # type: ignore[arg-type]
    with pytest.raises(PyrojRangeError):
        gregorian_to_jdn(2018, 13, 1)
    with pytest.raises(PyrojRangeError):
        persian_to_jdn(1397, 12, 30)
    with pytest.raises(PyrojRangeError):
        islamic_to_jdn(1439, 13, 1)


def test_gregorian_datetime_fractional_jdn_round_trip() -> None:
    dt = datetime(2018, 4, 10, 6, 30, 15, 123456)
    jdn = gregorian_datetime_to_jdn(dt)
    out = jdn_to_gregorian_datetime(jdn)
    assert abs((out - dt).total_seconds()) < 0.00002
