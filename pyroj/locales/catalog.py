"""Load locale month/weekday tables from ``catalog.json`` (package data)."""

from __future__ import annotations

import json
from importlib import resources
from typing import cast

from pyroj.locales.types import CalendarNames, LocaleData, LocaleId


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
    return LOCALE_BY_ID[locale_id]
