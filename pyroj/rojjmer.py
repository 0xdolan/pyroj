"""
Legacy ``Rojjmer`` API. Prefer :class:`pyroj.kurdish.KurdishDate` for new code.

Constructor ``(year, month, day)`` is **Gregorian** for :meth:`to_kurdish`, :meth:`hefte`,
:meth:`month_name`, and :meth:`is_leap`.

:meth:`to_gregorian` follows the old ``persiantools`` behavior: it treats the same three
numbers as a **Persian (Jalali)** calendar date (not Gregorian).
"""

from __future__ import annotations

import warnings
from datetime import date

from pyroj._core.convert import is_persian_leap_year
from pyroj.kurdish import KurdishDate

_MONTH_AR = [
    ("خاکەلێوە", "نەورۆز"),
    ("بانەمەڕ", "گوڵان"),
    ("جۆزەردان", None),
    ("پووشپەڕ", None),
    ("گەلاوێژ", None),
    ("خەرمانان", None),
    ("ڕەزبەر", None),
    ("گەڵاڕێزان", "خەزەڵوەر"),
    ("سەرماوەز", None),
    ("بەفرانبار", None),
    ("ڕێبەندان", None),
    ("ڕەشەمێ", None),
]

_MONTH_LATIN = [
    ("Xakelêwe", "Newroz"),
    ("Banemeŕ", "Guĺan"),
    ("Cozerdan", None),
    ("Pûşpeŕ", None),
    ("Gelawêj", None),
    ("Xermanan", None),
    ("Ŕezber", None),
    ("Geĺaŕêzan", "Xezeĺwer"),
    ("Sermawez", None),
    ("Befranbar", None),
    ("Ŕêbendan", None),
    ("Ŕeşemê", None),
]

_WEEK_AR = (
    "شەممە",
    "یەکشەممە",
    "دووشەممە",
    "سێشەممە",
    "چوارشەممە",
    "پێنجشەممە",
    "هەینی",
)
_WEEK_LATIN = (
    "Şemme",
    "Yekşemme",
    "Dûşemme",
    "Sêşemme",
    "Çwarşemme",
    "Pêncşemme",
    "Heynî",
)


class Rojjmer:
    """Kurdish calendar helper (legacy). Use :class:`KurdishDate` instead."""

    def __init__(self, year: int, month: int, day: int) -> None:
        self.year = year
        self.month = month
        self.day = day
        self.whole_year = date(self.year, self.month, self.day)

    def is_leap(self, solar: bool = False) -> bool:  # noqa: ARG002
        """True if the Persian (Jalali) year for ``whole_year`` is a leap year."""
        kd = KurdishDate.from_gregorian(self.whole_year)
        return is_persian_leap_year(kd.persian_year)

    def to_kurdish(self, solar: bool = False) -> KurdishDate:
        """
        Kurdish solar date.

        * ``solar=False`` (default): use **Gregorian** ``whole_year``.
        * ``solar=True``: ``(year, month, day)`` are **Persian (Jalali)**.
        """
        if solar:
            warnings.warn(
                "to_kurdish(solar=True) uses Persian (y, m, d); "
                "prefer KurdishDate.from_persian(...).",
                DeprecationWarning,
                stacklevel=2,
            )
            return KurdishDate.from_persian(self.year, self.month, self.day)
        return KurdishDate.from_gregorian(self.whole_year)

    def to_gregorian(self) -> date:
        """Convert **Persian** ``(year, month, day)`` (same triple as ``__init__``) to Gregorian."""
        return KurdishDate.from_persian(self.year, self.month, self.day).to_gregorian()

    def hefte(self, abbr: bool = False, latin: bool = False, solar: bool = False) -> str:  # noqa: ARG002
        """Weekday name; based on **Gregorian** ``whole_year`` (Saturday = first table entry)."""
        idx = (self.whole_year.weekday() + 2) % 7
        if latin:
            name = _WEEK_LATIN[idx]
            return name[0] if abbr else name
        name = _WEEK_AR[idx]
        return name[0] if abbr else name

    def month_name(self, second_name: bool = False, latin: bool = False) -> str:
        """Month name for the Kurdish month corresponding to **Gregorian** ``whole_year``."""
        ku_month = KurdishDate.from_gregorian(self.whole_year).month
        primary, secondary = (_MONTH_LATIN if latin else _MONTH_AR)[ku_month - 1]
        if second_name and secondary is not None:
            return secondary
        return primary
