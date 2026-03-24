"""Safe formatting (fixed tokens only)."""

from datetime import date

import pytest

from pyroj import (
    CalendarKind,
    KurdishDate,
    KurdishDateTime,
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


def test_format_kurdish_kmr_locale_month() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale=LocaleId.KMR,
    )
    assert "Xakel" in s


def test_format_kurdish_ckb_locale_month_from_code() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="ckb",
    )
    assert "خاک" in s


def test_format_kurdish_ckb_variant_standard_uses_xezelwer() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 11, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="ckb",
        kurdish_variant="standard",
    )
    assert "خەزەڵوەر" in s


def test_format_kurdish_kmr_variant_switches_month_name() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 11, 10))
    standard = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="kmr",
        kurdish_variant="standard",
    )
    gelarezan = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="kmr",
        kurdish_variant="gelarêzan",
    )
    assert standard == "Xezelwer"
    assert gelarezan == "Gelarêzan"


def test_format_kurdish_variant_with_dialect_alias_code() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 11, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="sdh",
        kurdish_variant="standard",
    )
    assert s == "خەزەڵوەر"


def test_format_kurdish_wikipedia_variants_for_all_requested_dialects() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    assert (
        format_calendar_date(
            kd,
            "%B",
            calendar=CalendarKind.KURDISH,
            locale="sdh",
            kurdish_variant="sdh_kelhuri",
        )
        == "جەشنان"
    )
    assert (
        format_calendar_date(
            kd,
            "%B",
            calendar=CalendarKind.KURDISH,
            locale="lki",
            kurdish_variant="lki_laki",
        )
        == "پەنجە"
    )
    assert (
        format_calendar_date(
            kd,
            "%B",
            calendar=CalendarKind.KURDISH,
            locale="hac",
            kurdish_variant="hac_hawrami",
        )
        == "نەوڕۆز"
    )
    assert (
        format_calendar_date(
            kd,
            "%B",
            calendar=CalendarKind.KURDISH,
            locale="zza",
            kurdish_variant="zza_zazaki",
        )
        == "Nîsanê/Lîzan"
    )
    assert (
        format_calendar_date(
            kd,
            "%B",
            calendar=CalendarKind.KURDISH,
            locale="kmr",
            kurdish_variant="kmr_wikipedia",
        )
        == "Nîsan"
    )


def test_unknown_kurdish_variant_falls_back_to_locale_default() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    s = format_calendar_date(
        kd,
        "%B",
        calendar=CalendarKind.KURDISH,
        locale="kmr",
        kurdish_variant="does_not_exist",
    )
    assert s == "Xakelêwe"


def test_locale_digits() -> None:
    loc = get_locale(LocaleId.FA)
    out = to_locale_digits("2718", loc)
    assert out == "۲۷۱۸"
    assert all(ord(ch) > 127 for ch in out)


def test_kmr_and_ckb_digits_differ() -> None:
    kd = KurdishDate.from_gregorian(date(2018, 4, 10))
    kmr = format_calendar_date(kd, "%Y", locale=LocaleId.KMR, use_locale_digits=True)
    ckb = format_calendar_date(kd, "%Y", locale=LocaleId.CKB, use_locale_digits=True)
    assert kmr == "2718"
    assert ckb == "٢٧١٨"


def test_datetime_percent_p_uses_locale_am_pm() -> None:
    kdt_am = KurdishDateTime(2726, 1, 3, hour=10, minute=15, second=0)
    kdt_pm = KurdishDateTime(2726, 1, 3, hour=15, minute=15, second=0)
    assert "berî niweroj" in kdt_am.strftime("%p", locale=LocaleId.KMR)
    assert "د.ن" in kdt_pm.strftime("%p", locale=LocaleId.CKB)


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
