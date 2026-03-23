"""Legacy Rojjmer behavior (Gregorian constructor)."""

from datetime import date

from pyroj.rojjmer import Rojjmer


def test_to_kurdish_gregorian() -> None:
    cal = Rojjmer(2018, 4, 10)
    kd = cal.to_kurdish()
    assert kd.year == 2718
    assert kd.month == 1
    assert kd.day == 21


def test_month_name() -> None:
    cal = Rojjmer(2021, 3, 21)
    assert "خاکەلێوە" in cal.month_name() or cal.month_name().startswith("خاک")


def test_to_gregorian_from_persian_triple() -> None:
    """Legacy: ``JalaliDate(1399, 10, 8).to_gregorian()`` → 2020-12-28."""
    cal = Rojjmer(1399, 10, 8)
    assert cal.to_gregorian() == date(2020, 12, 28)
