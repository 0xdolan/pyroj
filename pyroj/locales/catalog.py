"""Load locale month/weekday tables from ``catalog.json`` (package data)."""

from __future__ import annotations

import json
from importlib import resources
from typing import cast

from pyroj.locales.types import CalendarNames, LocaleData, LocaleId

_LOCALE_ALIASES: dict[str, LocaleId] = {
    "en": LocaleId.EN,
    "ku": LocaleId.KU,
    "kmr": LocaleId.KMR,
    "ckb": LocaleId.CKB,
    "fa": LocaleId.FA,
    "tr": LocaleId.TR,
    "ar": LocaleId.AR,
    # Script aliases
    "ku-latn": LocaleId.KMR,
    "ku_latn": LocaleId.KMR,
}

# Keep KU as a compatibility alias that resolves to Sorani/Arabic tables by default.
_COMPAT_LOCALE_REDIRECTS: dict[LocaleId, LocaleId] = {
    LocaleId.KU: LocaleId.CKB,
}


def _calendar_names(obj: object) -> CalendarNames:
    d = obj if isinstance(obj, dict) else {}
    return CalendarNames(
        months=tuple(d["months"]),
        months_short=tuple(d["months_short"]),
        weekdays=tuple(d["weekdays"]),
        weekdays_short=tuple(d["weekdays_short"]),
        weekdays_min=tuple(d["weekdays_min"]),
    )


def _load_raw() -> dict[str, object]:
    text = resources.files("pyroj.locales").joinpath("catalog.json").read_text(encoding="utf-8")
    data: object = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("catalog.json must contain a JSON object at the root")
    return cast(dict[str, object], data)


def _build_locale_by_id() -> dict[LocaleId, LocaleData]:
    raw = _load_raw()
    locales = raw["locales"]
    if not isinstance(locales, dict):
        raise ValueError("catalog.json: invalid 'locales'")
    out: dict[LocaleId, LocaleData] = {}
    for key, block in locales.items():
        if not isinstance(block, dict):
            continue
        lid = LocaleId[str(key).upper()]
        out[lid] = LocaleData(
            locale_id=lid,
            gregorian=_calendar_names(block["gregorian"]),
            persian=_calendar_names(block["persian"]),
            kurdish=_calendar_names(block["kurdish"]),
            islamic=_calendar_names(block["islamic"]),
            digits=tuple(block["digits"]),
            am_pm=(block["am_pm"][0], block["am_pm"][1]),
        )
    return out


LOCALE_BY_ID: dict[LocaleId, LocaleData] = _build_locale_by_id()


def get_locale(locale_id: LocaleId) -> LocaleData:
    """Return :class:`LocaleData` for ``locale_id``."""
    return LOCALE_BY_ID[resolve_locale(locale_id)]


def resolve_locale(locale: LocaleId | str, *, default: LocaleId = LocaleId.EN) -> LocaleId:
    """Resolve enum/string locale input to a known ``LocaleId`` with deterministic fallback."""
    lid = _resolve_locale_input(locale)
    if lid is None:
        return default
    normalized = _COMPAT_LOCALE_REDIRECTS.get(lid, lid)
    if normalized in LOCALE_BY_ID:
        return normalized
    return default


def get_locale_resolved(locale: LocaleId | str, *, default: LocaleId = LocaleId.EN) -> LocaleData:
    """Resolve ``locale`` then return its locale data."""
    return LOCALE_BY_ID[resolve_locale(locale, default=default)]


def _resolve_locale_input(locale: LocaleId | str) -> LocaleId | None:
    if isinstance(locale, LocaleId):
        return locale
    key = locale.strip().lower()
    if not key:
        return None
    direct = _LOCALE_ALIASES.get(key)
    if direct is not None:
        return direct
    enum_key = key.replace("-", "_").upper()
    if enum_key in LocaleId.__members__:
        return LocaleId[enum_key]
    return None
