"""
Safe date formatting: only fixed calendar tokens (no eval, no str.format user fields).

Patterns are scanned left-to-right; only known tokens are interpreted; all other characters
are copied literally (Unicode-safe).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

from pyroj.exceptions import PyrojValueError
from pyroj.kurdish import KurdishDate
from pyroj.locales.catalog import get_kurdish_month_variant, get_locale_resolved
from pyroj.locales.types import CalendarKind, LocaleData, LocaleId

# Map standard strftime tokens
_FORMAT_TOKENS: tuple[str, ...] = (
    "%Y",   # YYYY
    "%B",   # MMMM
    "%b",   # MMM
    "%m",   # MM
    "%y",   # YY
    "%d",   # DD
    "%A",   # dddd
    "%a",   # ddd
    "%w",   # d (weekday number)
    "%-w",  # d (no zero padding)
    "%-m",  # M
    "%-d",  # D
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
        if tok == "%Y":
            return f"{y:04d}"
        if tok == "%y":
            return f"{y % 100:02d}"
        if tok == "%B":
            return cn.months[m - 1]
        if tok == "%b":
            return cn.months_short[m - 1]
        if tok == "%m":
            return f"{m:02d}"
        if tok == "%-m":
            return str(m)
        if tok == "%d":
            return f"{d:02d}"
        if tok == "%-d":
            return str(d)
        if tok == "%A":
            return cn.weekdays[wi]
        if tok == "%a":
            return cn.weekdays_short[wi]
        if tok == "%w":
            return str(wi + 1)
        if tok == "%-w":
            return str(self.kd.weekday_persian())
        raise PyrojValueError(f"unknown internal token {tok!r}")


def format_calendar_date(
    kd: KurdishDate,
    pattern: str,
    *,
    calendar: CalendarKind = CalendarKind.KURDISH,
    locale: LocaleId | str = LocaleId.EN,
    kurdish_variant: str | None = None,
    use_locale_digits: bool = False,
) -> str:
    """
    Format ``kd`` using a standard ``strftime`` token vocabulary safely.

    Tokens: ``%Y``, ``%y``, ``%B``, ``%b``, ``%m``, ``%-m``,
    ``%d``, ``%-d``, ``%A``, ``%a``, ``%w`` (weekday index 1–7), ``%-w`` (weekday number).

    All other characters are copied literally.
    """
    if not isinstance(pattern, str):
        raise PyrojValueError("pattern must be str")
    if len(pattern) > _MAX_PATTERN_LEN:
        raise PyrojValueError(f"pattern exceeds max length {_MAX_PATTERN_LEN}")

    loc = get_locale_resolved(locale)
    if calendar is CalendarKind.KURDISH and kurdish_variant is not None:
        variant_names = get_kurdish_month_variant(locale, kurdish_variant)
        if variant_names is not None:
            loc = replace(loc, kurdish=variant_names)
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
    locale: LocaleId | str = LocaleId.EN,
    kurdish_variant: str | None = None,
    use_locale_digits: bool = False,
) -> str:
    """``%Y-%m-%d`` in the selected calendar’s year/month/day."""
    return format_calendar_date(
        kd,
        "%Y-%m-%d",
        calendar=calendar,
        locale=locale,
        kurdish_variant=kurdish_variant,
        use_locale_digits=use_locale_digits,
    )


_SUSPICIOUS = re.compile(r"[{}]")


def validate_pattern_safe(pattern: str) -> None:
    """Raise if ``pattern`` contains ``{`` or ``}`` (not used by this formatter)."""
    if _SUSPICIOUS.search(pattern):
        raise PyrojValueError(
            "pattern must not contain '{' or '}'; "
            "use fixed % tokens only (see format_calendar_date docstring)"
        )
