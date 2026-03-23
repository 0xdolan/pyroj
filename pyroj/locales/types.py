"""Locale identifiers and calendar name bundles (stdlib-only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class LocaleId(Enum):
    """Supported display locales."""

    EN = auto()  #: English (Latin)
    KU = auto()  #: Kurdish (Kurmanji-style tables, Arabic script)
    FA = auto()  #: Persian / Farsi
    TR = auto()  #: Turkish (Gregorian/Islamic Turkish; Kurdish solar Latin)
    AR = auto()  #: Arabic script (MSA-style month names where applicable)


class CalendarKind(Enum):
    """Which calendar’s month and weekday names to use when formatting."""

    GREGORIAN = auto()
    PERSIAN = auto()
    KURDISH = auto()
    ISLAMIC = auto()


@dataclass(frozen=True, slots=True)
class CalendarNames:
    """Twelve months and seven weekdays (weekday order: Saturday-first, matching KurdishDate)."""

    months: tuple[str, ...]
    months_short: tuple[str, ...]
    weekdays: tuple[str, ...]
    weekdays_short: tuple[str, ...]
    weekdays_min: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.months) != 12 or len(self.months_short) != 12:
            raise ValueError("months and months_short must have length 12")
        for seq in (self.weekdays, self.weekdays_short, self.weekdays_min):
            if len(seq) != 7:
                raise ValueError("weekday sequences must have length 7")


@dataclass(frozen=True, slots=True)
class LocaleData:
    """Labels for Gregorian, Persian, Kurdish solar, and tabular Islamic; digit shapes; AM/PM."""

    locale_id: LocaleId
    gregorian: CalendarNames
    persian: CalendarNames
    kurdish: CalendarNames
    islamic: CalendarNames
    digits: tuple[str, ...]
    am_pm: tuple[str, str]

    def __post_init__(self) -> None:
        if len(self.digits) != 10:
            raise ValueError("digits must have length 10")
        if len(self.am_pm) != 2:
            raise ValueError("am_pm must be (am, pm)")

    def names(self, kind: CalendarKind) -> CalendarNames:
        return {
            CalendarKind.GREGORIAN: self.gregorian,
            CalendarKind.PERSIAN: self.persian,
            CalendarKind.KURDISH: self.kurdish,
            CalendarKind.ISLAMIC: self.islamic,
        }[kind]
