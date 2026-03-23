"""Locale tables for month and weekday names (Gregorian, Persian, Kurdish solar, Islamic)."""

from pyroj.locales.catalog import LOCALE_BY_ID, get_locale
from pyroj.locales.types import CalendarKind, CalendarNames, LocaleData, LocaleId

__all__ = [
    "CalendarKind",
    "CalendarNames",
    "LOCALE_BY_ID",
    "LocaleData",
    "LocaleId",
    "get_locale",
]
