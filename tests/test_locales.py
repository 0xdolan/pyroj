"""Locale catalog integrity."""

from pyroj.locales.catalog import LOCALE_BY_ID, resolve_locale
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
        LocaleId.KMR,
        LocaleId.CKB,
        LocaleId.KU,
        LocaleId.FA,
        LocaleId.TR,
        LocaleId.AR,
    }


def test_locale_resolution_aliases_and_fallback() -> None:
    assert resolve_locale("kmr") is LocaleId.KMR
    assert resolve_locale("ckb") is LocaleId.CKB
    assert resolve_locale("sdh") is LocaleId.CKB
    assert resolve_locale("lki") is LocaleId.CKB
    assert resolve_locale("hac") is LocaleId.CKB
    assert resolve_locale("zza") is LocaleId.KMR
    assert resolve_locale("diq") is LocaleId.KMR
    assert resolve_locale("kiu") is LocaleId.KMR
    assert resolve_locale("ku-latn") is LocaleId.KMR
    # Backward-compatible alias behavior.
    assert resolve_locale("ku") is LocaleId.CKB
    assert resolve_locale(LocaleId.KU) is LocaleId.CKB
    # Deterministic fallback.
    assert resolve_locale("unknown-locale") is LocaleId.EN
