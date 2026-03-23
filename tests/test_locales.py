"""Locale catalog integrity."""

from pyroj.locales.catalog import LOCALE_BY_ID
from pyroj.locales.types import CalendarKind, LocaleId


def test_all_locales_have_twelve_months() -> None:
    for lid, data in LOCALE_BY_ID.items():
        for kind in CalendarKind:
            cn = data.names(kind)
            assert len(cn.months) == 12
            assert len(cn.months_short) == 12
            assert len(cn.weekdays) == 7


def test_locale_ids_complete() -> None:
    assert set(LOCALE_BY_ID.keys()) == {
        LocaleId.EN,
        LocaleId.KU,
        LocaleId.FA,
        LocaleId.TR,
        LocaleId.AR,
    }
