"""
Kurdish solar calendar date (Persian/Jalali structure with +1321 year offset).

This matches the KurdishDate TypeScript reference and legacy pyroj behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto

from pyroj._core.convert import (
    KURDISH_SOLAR_YEAR_OFFSET,
    MAX_SUPPORTED_YEAR,
    MIN_SUPPORTED_YEAR,
    gregorian_to_jdn,
    islamic_to_jdn,
    jdn_to_gregorian,
    jdn_to_gregorian_datetime,
    jdn_to_islamic,
    jdn_to_persian,
    persian_days_in_month,
    persian_to_jdn,
    persian_weekday_from_gregorian,
)
from pyroj.exceptions import PyrojRangeError, PyrojValueError


def _require_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise PyrojValueError(f"{name} must be int (bool is not allowed)")
    return value


def _require_year(year: int) -> int:
    if year < MIN_SUPPORTED_YEAR or year > MAX_SUPPORTED_YEAR:
        raise PyrojRangeError(
            f"year must be in [{MIN_SUPPORTED_YEAR}, {MAX_SUPPORTED_YEAR}], got {year}"
        )
    return year


class KurdishEra(Enum):
    """How Kurdish ``year`` is counted."""

    #: Kurdish year = Jalali year + 1321 (used by Kurdipedia-style tools and this library).
    SOLAR_PERSIAN_OFFSET = auto()


@dataclass(frozen=True, order=False)
class KurdishDate:
    """
    Kurdish solar date: same month lengths as the Persian (Jalali) calendar, year = Persian + 1321.

    Behaves like an immutable date value: hashable when all fields are valid.
    """

    year: int
    month: int
    day: int
    era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET

    def __post_init__(self) -> None:
        _require_year(_require_int("year", self.year))
        _require_int("month", self.month)
        _require_int("day", self.day)
        if self.era is not KurdishEra.SOLAR_PERSIAN_OFFSET:
            raise PyrojValueError(f"Unsupported era: {self.era!r}")
        if self.month < 1 or self.month > 12:
            raise PyrojRangeError(f"month must be 1..12, got {self.month}")
        py = self.persian_year
        dim = persian_days_in_month(py, self.month)
        if self.day < 1 or self.day > dim:
            raise PyrojRangeError(
                f"day {self.day} out of range for Kurdish month {self.month} (max {dim})"
            )

    @property
    def persian_year(self) -> int:
        """Persian (Jalali) calendar year (``Kurdish year − 1321``)."""
        return self.year - KURDISH_SOLAR_YEAR_OFFSET

    @property
    def _jdn(self) -> float:
        return persian_to_jdn(self.persian_year, self.month, self.day)

    @classmethod
    def from_gregorian(
        cls, d: date, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> KurdishDate:
        """Build from a Gregorian :class:`datetime.date`."""
        if not isinstance(d, date):
            raise PyrojValueError("d must be datetime.date")
        j = gregorian_to_jdn(d.year, d.month, d.day)
        py, pm, pd = jdn_to_persian(j)
        return cls(py + KURDISH_SOLAR_YEAR_OFFSET, pm, pd, era=era)

    @classmethod
    def from_persian(
        cls, year: int, month: int, day: int, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> KurdishDate:
        """Build from a Persian (Jalali) calendar date."""
        return cls(year + KURDISH_SOLAR_YEAR_OFFSET, month, day, era=era)

    @classmethod
    def from_kurdish_solar(
        cls, year: int, month: int, day: int, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> KurdishDate:
        """Validate and construct when ``year`` is already the Kurdish solar year."""
        return cls(year, month, day, era=era)

    def to_gregorian(self) -> date:
        """Convert to a proleptic Gregorian :class:`datetime.date`."""
        y, m, d = jdn_to_gregorian(self._jdn)
        return date(y, m, d)

    @classmethod
    def from_jdn(
        cls, jdn: float, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> KurdishDate:
        """Build KurdishDate from Julian Day Number (JDN)."""
        py, pm, pd = jdn_to_persian(jdn)
        return cls(py + KURDISH_SOLAR_YEAR_OFFSET, pm, pd, era=era)

    def to_jdn(self) -> float:
        """Return Julian Day Number (JDN) for this Kurdish date at local midnight."""
        return self._jdn

    def to_datetime(self) -> datetime:
        """Return Gregorian naive datetime at midnight for this Kurdish date."""
        return jdn_to_gregorian_datetime(self._jdn)

    def to_persian(self) -> tuple[int, int, int]:
        """Persian (Jalali) ``(year, month, day)``."""
        py, pm, pd = jdn_to_persian(self._jdn)
        return py, pm, pd

    def to_islamic(self) -> tuple[int, int, int]:
        """Tabular Islamic ``(year, month, day)`` (same model as KurdishDate)."""
        return jdn_to_islamic(self._jdn)

    def weekday_persian(self) -> int:
        """Weekday index 1..7 compatible with KurdishDate ``day()`` (locale tables)."""
        return persian_weekday_from_gregorian(self.to_gregorian())

    def replace(
        self, year: int | None = None, month: int | None = None, day: int | None = None
    ) -> KurdishDate:
        """Return a new date with replaced fields (same idea as :meth:`datetime.date.replace`)."""
        return KurdishDate(
            year if year is not None else self.year,
            month if month is not None else self.month,
            day if day is not None else self.day,
            era=self.era,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KurdishDate):
            return NotImplemented
        return (
            self.year,
            self.month,
            self.day,
            self.era,
        ) == (other.year, other.month, other.day, other.era)

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day, self.era))

    def __lt__(self, other: KurdishDate) -> bool:
        if not isinstance(other, KurdishDate):
            return NotImplemented
        return self._jdn < other._jdn

    def __le__(self, other: KurdishDate) -> bool:
        if not isinstance(other, KurdishDate):
            return NotImplemented
        return self._jdn <= other._jdn

    def __gt__(self, other: KurdishDate) -> bool:
        if not isinstance(other, KurdishDate):
            return NotImplemented
        return self._jdn > other._jdn

    def __ge__(self, other: KurdishDate) -> bool:
        if not isinstance(other, KurdishDate):
            return NotImplemented
        return self._jdn >= other._jdn

    def __repr__(self) -> str:
        return f"KurdishDate({self.year}, {self.month}, {self.day})"

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"


def gregorian_to_islamic(d: date) -> tuple[int, int, int]:
    """Tabular Islamic date for a Gregorian day."""
    return jdn_to_islamic(gregorian_to_jdn(d.year, d.month, d.day))


def gregorian_to_persian(d: date) -> tuple[int, int, int]:
    """Persian (Jalali) date for a Gregorian day."""
    return jdn_to_persian(gregorian_to_jdn(d.year, d.month, d.day))


def islamic_to_gregorian(year: int, month: int, day: int) -> date:
    """Gregorian date for a tabular Islamic date."""
    _require_year(_require_int("year", year))
    _require_int("month", month)
    _require_int("day", day)
    j = islamic_to_jdn(year, month, day)
    y, m, d = jdn_to_gregorian(j)
    return date(y, m, d)


def persian_to_gregorian(year: int, month: int, day: int) -> date:
    """Gregorian date for a Persian (Jalali) date."""
    _require_year(_require_int("year", year))
    _require_int("month", month)
    _require_int("day", day)
    j = persian_to_jdn(year, month, day)
    y, m, d = jdn_to_gregorian(j)
    return date(y, m, d)
