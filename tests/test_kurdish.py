"""KurdishDate API tests."""

from datetime import date

import pytest

from pyroj import KurdishDate
from pyroj.exceptions import PyrojRangeError, PyrojValueError


def test_from_gregorian_april_10_2018() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert kd.year == 2718
    assert kd.month == 1
    assert kd.day == 21
    assert kd.persian_year == 1397


def test_from_persian() -> None:
    kd = KurdishDate.from_persian(1397, 1, 21)
    assert kd.year == 2718
    assert kd.to_gregorian() == date(2018, 4, 10)


def test_to_islamic() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert kd.to_islamic() == (1439, 7, 24)


def test_replace() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert kd.replace(day=1).day == 1


def test_ordering() -> None:
    a = KurdishDate.from_gregorian(date(2018, 4, 10))
    b = KurdishDate.from_gregorian(date(2018, 4, 11))
    assert a < b


def test_invalid_day() -> None:
    with pytest.raises(PyrojRangeError):
        KurdishDate.from_kurdish_solar(2718, 1, 32)


def test_hash() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert hash(kd) == hash(KurdishDate(2718, 1, 21))


def test_kurdish_rejects_bool_and_year_bounds() -> None:
    with pytest.raises(PyrojValueError):
        KurdishDate.from_kurdish_solar(2718, True, 21)  # type: ignore[arg-type]
    with pytest.raises(PyrojRangeError):
        KurdishDate.from_kurdish_solar(10000, 1, 1)


def test_kurdish_to_from_jdn_round_trip() -> None:
    kd = KurdishDate.from_kurdish_solar(2718, 1, 21)
    jdn = kd.to_jdn()
    out = KurdishDate.from_jdn(jdn)
    assert out == kd
