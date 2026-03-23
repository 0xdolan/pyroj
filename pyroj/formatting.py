"""
Safe date formatting: only fixed calendar tokens (no eval, no str.format user fields).

Patterns are scanned left-to-right; only known tokens are interpreted; all other characters
are copied literally (Unicode-safe).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from pyroj.exceptions import PyrojValueError
from pyroj.kurdish import KurdishDate
from pyroj.locales.catalog import get_locale
from pyroj.locales.types import CalendarKind, LocaleData, LocaleId

# Longest token first (see _tokenize)
_FORMAT_TOKENS: tuple[str, ...] = (
    "YYYY",
    "MMMM",
    "MMM",
    "MM",
    "YY",
    "DD",
    "dddd",
    "ddd",
    "dd",
    "WW",
    "M",
    "D",
    "d",
)

_MAX_PATTERN_LEN = 512


def to_locale_digits(numeric_string: str, locale: LocaleData) -> str:
    """Replace ASCII 0-9 with the locale’s digit shapes."""
    out: list[str] = []
    for ch in numeric_string:
        if ch.isdigit():
            out.append(locale.digits[int(ch)])
        else:
            out.append(ch)
    return "".join(out)


def _tokenize(pattern: str) -> list[tuple[str, str]]:
    """Split ``pattern`` into ``('t', token)`` or ``('l', char)`` entries."""
    parts: list[tuple[str, str]] = []
    i = 0
    while i < len(pattern):
        matched = False
        for tok in _FORMAT_TOKENS:
            if pattern.startswith(tok, i):
                parts.append(("t", tok))
                i += len(tok)
                matched = True
                break
        if not matched:
            parts.append(("l", pattern[i]))
            i += 1
    return parts


def _ymd_for_calendar(kd: KurdishDate, kind: CalendarKind) -> tuple[int, int, int]:
    if kind is CalendarKind.KURDISH:
        return kd.year, kd.month, kd.day
    if kind is CalendarKind.PERSIAN:
        return kd.to_persian()
    if kind is CalendarKind.ISLAMIC:
        return kd.to_islamic()
    g = kd.to_gregorian()
    return g.year, g.month, g.day


def _weekday_index(kd: KurdishDate, kind: CalendarKind) -> int:
    """Index into ``CalendarNames.weekdays*`` (Monday-first for Gregorian, Saturday-first else)."""
    g = kd.to_gregorian()
    if kind is CalendarKind.GREGORIAN:
        return g.weekday()  # Monday=0 .. Sunday=6
    return kd.weekday_persian() - 1  # Saturday=0 .. Friday=6


@dataclass(slots=True)
class _Render:
    kd: KurdishDate
    kind: CalendarKind
    locale: LocaleData

    def render(self, tok: str) -> str:
        y, m, d = _ymd_for_calendar(self.kd, self.kind)
        cn = self.locale.names(self.kind)
        wi = _weekday_index(self.kd, self.kind)
        if tok == "YYYY":
            return f"{y:04d}"
        if tok == "YY":
            return f"{y % 100:02d}"
        if tok == "MMMM":
            return cn.months[m - 1]
        if tok == "MMM":
            return cn.months_short[m - 1]
        if tok == "MM":
            return f"{m:02d}"
        if tok == "M":
            return str(m)
        if tok == "DD":
            return f"{d:02d}"
        if tok == "D":
            return str(d)
        if tok == "dddd":
            return cn.weekdays[wi]
        if tok == "ddd":
            return cn.weekdays_short[wi]
        if tok == "dd":
            return cn.weekdays_min[wi]
        if tok == "d":
            return str(self.kd.weekday_persian())
        if tok == "WW":
            return str(wi + 1)
        raise PyrojValueError(f"unknown internal token {tok!r}")


def format_calendar_date(
    kd: KurdishDate,
    pattern: str,
    *,
    calendar: CalendarKind = CalendarKind.KURDISH,
    locale: LocaleId = LocaleId.EN,
    use_locale_digits: bool = False,
) -> str:
    """
    Format ``kd`` using a **fixed token vocabulary** (no ``eval``, no user ``str.format``).

    Tokens (longest match wins): ``YYYY``, ``YY``, ``MMMM``, ``MMM``, ``MM``, ``M``,
    ``DD``, ``D``, ``dddd``, ``ddd``, ``dd`` (weekday min), ``d`` (weekday number 1–7),
    ``WW`` (weekday index 1–7 in the current calendar’s weekday order).

    All other characters are copied literally.
    """
    if not isinstance(pattern, str):
        raise PyrojValueError("pattern must be str")
    if len(pattern) > _MAX_PATTERN_LEN:
        raise PyrojValueError(f"pattern exceeds max length {_MAX_PATTERN_LEN}")

    loc = get_locale(locale)
    validate_pattern_safe(pattern)
    ctx = _Render(kd=kd, kind=calendar, locale=loc)
    out: list[str] = []
    for seg_kind, seg_val in _tokenize(pattern):
        if seg_kind == "l":
            out.append(seg_val)
        else:
            out.append(ctx.render(seg_val))
    result = "".join(out)
    if use_locale_digits:
        return to_locale_digits(result, loc)
    return result


def format_iso_date(
    kd: KurdishDate,
    *,
    calendar: CalendarKind = CalendarKind.KURDISH,
    locale: LocaleId = LocaleId.EN,
    use_locale_digits: bool = False,
) -> str:
    """``YYYY-MM-DD`` in the selected calendar’s year/month/day."""
    return format_calendar_date(
        kd,
        "YYYY-MM-DD",
        calendar=calendar,
        locale=locale,
        use_locale_digits=use_locale_digits,
    )


_SUSPICIOUS = re.compile(r"[{}%]")


def validate_pattern_safe(pattern: str) -> None:
    """Raise if ``pattern`` contains ``{``, ``}``, or ``%`` (not used by this formatter)."""
    if _SUSPICIOUS.search(pattern):
        raise PyrojValueError(
            "pattern must not contain '{', '}', or '%'; "
            "use fixed tokens only (see format_calendar_date docstring)"
        )
