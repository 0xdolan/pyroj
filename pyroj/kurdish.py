"""
Kurdish solar calendar date (Persian/Jalali structure with +1321 year offset).

Provides dynamic date and datetime objects fully compatible with Python's built-in datetime module.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, tzinfo
from enum import Enum, auto
from typing import Any, TypeVar

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
from pyroj.locales import LocaleId

_TDate = TypeVar("_TDate", bound="KurdishDate")
_TDateTime = TypeVar("_TDateTime", bound="KurdishDateTime")

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
    #: Kurdish year = Jalali year + 1321 (Median Empire Epoch, 700 BC)
    SOLAR_PERSIAN_OFFSET = auto()
    #: Kurdish year = Jalali year + 1233 (Fall of Nineveh Epoch, 612 BC)
    FALL_OF_NINEVEH = auto()

    def from_persian_year(self, p_year: int) -> int:
        if self == KurdishEra.SOLAR_PERSIAN_OFFSET:
            return p_year + KURDISH_SOLAR_YEAR_OFFSET
        if self == KurdishEra.FALL_OF_NINEVEH:
            return p_year + 1233
        return p_year

    def to_persian_year(self, k_year: int) -> int:
        if self == KurdishEra.SOLAR_PERSIAN_OFFSET:
            return k_year - KURDISH_SOLAR_YEAR_OFFSET
        if self == KurdishEra.FALL_OF_NINEVEH:
            return k_year - 1233
        return k_year


class KurdishDate(date):
    """
    Kurdish solar date: same month lengths as the Persian (Jalali) calendar.
    Inherits from `datetime.date`, so it can be used anywhere a standard Python date is expected.
    """
    
    _era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET

    def __new__(cls: type[_TDate], *args: Any, **kwargs: Any) -> _TDate:
        # Internal construction directly from Gregorian parameters
        if "_gregorian_date" in kwargs:
            g_date = kwargs.pop("_gregorian_date")
            era = kwargs.pop("era", KurdishEra.SOLAR_PERSIAN_OFFSET)
            obj = super().__new__(cls, g_date.year, g_date.month, g_date.day)
            obj._era = era
            return obj

        if len(args) == 3:
            year, month, day = args
        else:
            year = kwargs.get("year")
            month = kwargs.get("month")
            day = kwargs.get("day")
            if year is None or month is None or day is None:
                raise TypeError("KurdishDate takes exactly 3 arguments (year, month, day)")

        era = kwargs.get("era", KurdishEra.SOLAR_PERSIAN_OFFSET)
        
        _require_year(_require_int("year", year))
        _require_int("month", month)
        _require_int("day", day)

        if month < 1 or month > 12:
            raise PyrojRangeError(f"month must be 1..12, got {month}")
        
        py = era.to_persian_year(year)
        dim = persian_days_in_month(py, month)
        if day < 1 or day > dim:
            raise PyrojRangeError(
                f"day {day} out of range for Kurdish month {month} (max {dim})"
            )
        
        jdn = persian_to_jdn(py, month, day)
        gy, gm, gd = jdn_to_gregorian(jdn)
        
        obj = super().__new__(cls, gy, gm, gd)
        obj._era = era
        return obj

    @property
    def era(self) -> KurdishEra:
        """The epoch era used to calculate the year."""
        return self._era

    @property
    def persian_year(self) -> int:
        """Persian (Jalali) calendar year."""
        py, _, _ = jdn_to_persian(self._jdn)
        return py

    @property
    def year(self) -> int:
        """The Kurdish year."""
        return self._era.from_persian_year(self.persian_year)

    @property
    def month(self) -> int:
        """The Kurdish month."""
        _, pm, _ = jdn_to_persian(self._jdn)
        return pm

    @property
    def day(self) -> int:
        """The Kurdish day."""
        _, _, pd = jdn_to_persian(self._jdn)
        return pd

    @property
    def _jdn(self) -> float:
        """Returns the Julian Day Number for local midnight."""
        return self.toordinal() + 1721424.5

    @classmethod
    def from_gregorian(
        cls: type[_TDate], d: date, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> _TDate:
        """Build from a Gregorian :class:`datetime.date`."""
        if not isinstance(d, date):
            raise PyrojValueError("d must be datetime.date")
        return cls(_gregorian_date=d, era=era)

    @classmethod
    def from_persian(
        cls: type[_TDate],
        year: int,
        month: int,
        day: int,
        *,
        era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET,
    ) -> _TDate:
        """Build from a Persian (Jalali) calendar date."""
        return cls(era.from_persian_year(year), month, day, era=era)

    @classmethod
    def from_kurdish_solar(
        cls: type[_TDate],
        year: int,
        month: int,
        day: int,
        *,
        era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET,
    ) -> _TDate:
        """Construct when ``year`` is already the Kurdish solar year."""
        return cls(year, month, day, era=era)

    def to_gregorian(self) -> date:
        """Convert to a proleptic Gregorian :class:`datetime.date`."""
        return date(super().year, super().month, super().day)

    @classmethod
    def from_jdn(
        cls: type[_TDate], jdn: float, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> _TDate:
        """Build KurdishDate from Julian Day Number (JDN)."""
        gy, gm, gd = jdn_to_gregorian(jdn)
        return cls(_gregorian_date=date(gy, gm, gd), era=era)

    def to_jdn(self) -> float:
        """Return Julian Day Number (JDN) for this Kurdish date at local midnight."""
        return self._jdn

    def to_datetime(self) -> datetime:
        """Return Gregorian naive datetime at midnight for this Kurdish date."""
        return jdn_to_gregorian_datetime(self._jdn)

    def to_persian(self) -> tuple[int, int, int]:
        """Persian (Jalali) ``(year, month, day)``."""
        return jdn_to_persian(self._jdn)

    def to_islamic(self) -> tuple[int, int, int]:
        """Tabular Islamic ``(year, month, day)``."""
        return jdn_to_islamic(self._jdn)

    def weekday_persian(self) -> int:
        """Weekday index 1..7 (Saturday=1) compatible with Kurdish locale conventions."""
        return persian_weekday_from_gregorian(self.to_gregorian())

    def replace(  # type: ignore[override]
        self: _TDate,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        **kwargs: Any,
    ) -> _TDate:
        """Return a new :class:`KurdishDate` with replaced fields.
        
        Similar to :meth:`datetime.date.replace`.
        """
        return self.__class__(
            year if year is not None else self.year,
            month if month is not None else self.month,
            day if day is not None else self.day,
            era=kwargs.get("era", self.era),
        )

    def strftime(self, format: str, locale: LocaleId | str = LocaleId.EN) -> str:
        """Format building on standard % strftime directives, optionally with locale translation."""
        from pyroj.formatting import format_calendar_date
        
        # If passed string 'en', 'ku', convert to LocaleId if needed,
        # though get_locale might handle it.
        # But for safety:
        if isinstance(locale, str):
            locale = LocaleId(locale)
            
        return format_calendar_date(self, format, locale=locale)

    def __format__(self, format_spec: str) -> str:
        if not format_spec:
            return str(self)
        from pyroj.formatting import format_calendar_date
        return format_calendar_date(self, format_spec)

    def timetuple(self) -> Any:
        """Return time.struct_time compatible tuple, based on Gregorian."""
        return super().timetuple()

    def __add__(self, other: Any) -> KurdishDate:
        if isinstance(other, timedelta):
            # Calculate addition strictly on the Gregorian base to bypass invalid C allocations
            new_gregorian = self.to_gregorian() + other
            return self.__class__(_gregorian_date=new_gregorian, era=self.era)
        return NotImplemented

    def __radd__(self, other: Any) -> KurdishDate:
        return self.__add__(other)

    def __sub__(self, other: Any) -> KurdishDate | timedelta:  # type: ignore[override]
        if isinstance(other, timedelta):
            new_gregorian = self.to_gregorian() - other
            return self.__class__(_gregorian_date=new_gregorian, era=self.era)
        elif isinstance(other, date):
            if isinstance(other, KurdishDate):
                return self.to_gregorian() - other.to_gregorian()
            return self.to_gregorian() - other
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.year}, {self.month}, {self.day})"

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"


class KurdishDateTime(datetime):
    """
    Kurdish solar datetime: inherits from `datetime.datetime`.
    """

    _era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET

    def __new__(
        cls: type[_TDateTime],
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: tzinfo | None = None,
        *,
        fold: int = 0,
        **kwargs: Any
    ) -> _TDateTime:
        if "_gregorian_datetime" in kwargs:
            g_dt = kwargs.pop("_gregorian_datetime")
            era = kwargs.pop("era", KurdishEra.SOLAR_PERSIAN_OFFSET)
            obj = super().__new__(
                cls, g_dt.year, g_dt.month, g_dt.day,
                g_dt.hour, g_dt.minute, g_dt.second, g_dt.microsecond,
                tzinfo=g_dt.tzinfo, fold=g_dt.fold
            )
            obj._era = era
            return obj
            
        if year is None or month is None or day is None:
            raise TypeError("KurdishDateTime requires year, month, and day")
            
        era = kwargs.get("era", KurdishEra.SOLAR_PERSIAN_OFFSET)
        
        _require_year(_require_int("year", year))
        _require_int("month", month)
        _require_int("day", day)

        if month < 1 or month > 12:
            raise PyrojRangeError(f"month must be 1..12, got {month}")
            
        py = era.to_persian_year(year)
        dim = persian_days_in_month(py, month)
        if day < 1 or day > dim:
            raise PyrojRangeError(
                f"day {day} out of range for Kurdish month {month} (max {dim})"
            )
        
        jdn = persian_to_jdn(py, month, day)
        gy, gm, gd = jdn_to_gregorian(jdn)

        obj = super().__new__(
            cls, gy, gm, gd, hour, minute, second, microsecond, tzinfo=tzinfo, fold=fold
        )
        obj._era = era
        return obj

    @property
    def era(self) -> KurdishEra:
        """The epoch era used to calculate the year."""
        return self._era

    @property
    def persian_year(self) -> int:
        """Persian (Jalali) calendar year."""
        py, _, _ = jdn_to_persian(self._jdn)
        return py

    @property
    def year(self) -> int:
        return self._era.from_persian_year(self.persian_year)

    @property
    def month(self) -> int:
        _, pm, _ = jdn_to_persian(self._jdn)
        return pm

    @property
    def day(self) -> int:
        _, _, pd = jdn_to_persian(self._jdn)
        return pd

    @property
    def _jdn(self) -> float:
        """Returns the Julian Day Number for local midnight of this datetime."""
        return self.toordinal() + 1721424.5

    @classmethod
    def from_gregorian(
        cls: type[_TDateTime], dt: datetime, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET
    ) -> _TDateTime:
        if not isinstance(dt, datetime):
            raise PyrojValueError("dt must be datetime.datetime")
        return cls(_gregorian_datetime=dt, era=era)

    def to_gregorian(self) -> datetime:
        return datetime(
            super().year,
            super().month,
            super().day,
            self.hour, self.minute, self.second, self.microsecond, self.tzinfo, fold=self.fold
        )

    def replace(  # type: ignore[override]
        self: _TDateTime, 
        year: int | None = None, month: int | None = None, day: int | None = None,
        hour: int | None = None, minute: int | None = None, second: int | None = None,
        microsecond: int | None = None, tzinfo: tzinfo | Any = True,
        *args: Any, **kwargs: Any
    ) -> _TDateTime:
        tz = self.tzinfo if tzinfo is True else tzinfo
        return self.__class__(
            year if year is not None else self.year,
            month if month is not None else self.month,
            day if day is not None else self.day,
            hour if hour is not None else self.hour,
            minute if minute is not None else self.minute,
            second if second is not None else self.second,
            microsecond if microsecond is not None else self.microsecond,
            tzinfo=tz,
            fold=kwargs.get("fold", self.fold),
            era=kwargs.get("era", self.era)
        )

    def __add__(self, other: Any) -> KurdishDateTime:
        if isinstance(other, timedelta):
            new_gregorian = self.to_gregorian() + other
            return self.__class__(_gregorian_datetime=new_gregorian, era=self.era)
        return NotImplemented

    def __radd__(self, other: Any) -> KurdishDateTime:
        return self.__add__(other)

    def __sub__(self, other: Any) -> KurdishDateTime | timedelta:  # type: ignore[override]
        if isinstance(other, timedelta):
            new_gregorian = self.to_gregorian() - other
            return self.__class__(_gregorian_datetime=new_gregorian, era=self.era)
        elif isinstance(other, datetime):
            if isinstance(other, KurdishDateTime):
                return self.to_gregorian() - other.to_gregorian()
            return self.to_gregorian() - other
        return NotImplemented
        
    def date(self) -> KurdishDate:
        return KurdishDate(self.year, self.month, self.day, era=self.era)

    def strftime(self, format: str, locale: LocaleId | str = LocaleId.EN) -> str:
        """Format building on standard % strftime directives, with datetime extensions."""
        # Replace time tokens manually, then dispatch date tokens to formatting
        date_pattern = format.replace('%H', f"{self.hour:02d}")
        date_pattern = date_pattern.replace('%I', f"{(self.hour % 12) or 12:02d}")
        date_pattern = date_pattern.replace('%M', f"{self.minute:02d}")
        date_pattern = date_pattern.replace('%S', f"{self.second:02d}")
        date_pattern = date_pattern.replace('%f', f"{self.microsecond:06d}")
        date_pattern = date_pattern.replace('%p', "AM" if self.hour < 12 else "PM")
        
        if isinstance(locale, str):
            locale = LocaleId(locale)
            
        from pyroj.formatting import format_calendar_date
        return format_calendar_date(self.date(), date_pattern, locale=locale)

    def __format__(self, format_spec: str) -> str:
        if not format_spec:
            return str(self)
        return self.strftime(format_spec)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.year}, {self.month}, {self.day}, "
            f"{self.hour}, {self.minute}, {self.second})"
        )

    def __str__(self) -> str:
        s_date = f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        s_time = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        return f"{s_date} {s_time}"


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
