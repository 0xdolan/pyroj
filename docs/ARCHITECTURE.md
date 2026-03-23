# Pyroj v2 — Architecture (stdlib `datetime` only)

This document defines how the refactored **pyroj** library aligns with Python’s `datetime` module, how calendar math is performed without third-party packages, and how naming, locales, and security constraints fit together.

## Goals

- **Single runtime dependency**: the Python standard library (`datetime`, `logging`, `enum`, `typing`, `dataclasses` as needed). Calendar algorithms (Julian day number, Persian solar, tabular Islamic) are implemented in pure Python inside the package—no `persiantools`, no `hijri` wheels.
- **Interop first**: Kurdish calendar values are not opaque strings. They behave like `datetime.date` / `datetime.datetime` companions: comparable, hashable where appropriate, and convertible to/from `datetime.date` and `datetime.datetime`.
- **Extensibility**: Locale strings live in `pyroj/locales/catalog.json`; new display languages can be added by extending that file and `LocaleId` when needed.
- **Observability**: Structured logging (module-level loggers), no secrets in logs.
- **Safety**: Strict validation on construction; no `eval`, no unsafe deserialization; reject out-of-range dates with documented exceptions.

## Canonical time model

1. **Instant in civil time**: Represented as `datetime.datetime` (timezone-aware when the user supplies a `tzinfo`; naive when they do not). All arithmetic that involves hours/minutes/seconds/microseconds uses `timedelta` and follows `datetime` semantics.
2. **Date-only**: Represented as `datetime.date` for the Gregorian civil date of that instant in the same timezone context (or UTC for conversions that are defined only on the date part).
3. **Julian day (JDN)**: Internal hub for converting between Gregorian, Persian (Jalali), and tabular Islamic—same numerical approach as the reference implementation in `KurdishDate/src/dateConverter.ts` in this workspace. Floating JDN includes the fractional day for time-of-day.

This mirrors the **KurdishDate** TypeScript project: one Julian day value updates all calendar views.

## Kurdish year: two documented eras (must not be conflated)

Historical sources describe different epoch conventions:

| Mode | Rule (conceptual) | Used by |
|------|-------------------|---------|
| **Solar offset (default)** | Kurdish year = Persian (Jalali) year + **1321**; month/day match Persian solar structure. | Current `Rojjmer`, `kurdish-calendar.py`, `KurdishDate` TS, Kurdipedia-style outputs (e.g. 2726 for 1405 + 1321). |
| **Median / Nineveh era** | Year count tied to **612 BCE** and vernal equinox (Newroz); formulas such as `1 + (gregorian_year + 611)` appear in literature—**not** interchangeable with the +1321 solar calendar without explicit conversion. | Academic / cultural articles (Roshani, etc.). |

The v2 API must expose this as an explicit **`KurdishEra`** (or similarly named) enum so users and tests never mix eras silently.

## Package layout (current)

```
pyroj/
  _core/convert.py     # Julian day hub (Gregorian, Persian, Islamic)
  kurdish.py           # KurdishDate
  locales/catalog.json # Month/weekday strings per locale (loaded at import)
  locales/catalog.py   # Loader + LOCALE_BY_ID
  formatting.py        # Fixed-token date formatting
  exceptions.py
```

Naming follows **PEP 8**; `KurdishDate` mirrors `datetime.date` where practical (`replace`, ordering, hash).

## Types and behavior

### `KurdishDate` (date-only, v2)

- Fields: `year`, `month`, `day` in Kurdish **solar** calendar under selected `KurdishEra`.
- Construction: `from_gregorian(date: datetime.date)`, `from_persian(year, month, day)`, `from_jdn(jdn: float)`, etc.
- Conversion: `to_gregorian() -> datetime.date`, `to_persian() -> tuple[int,int,int]`, `to_islamic() -> ...`, `to_datetime(...) -> datetime.datetime` when time is zero or user-supplied.
- Implements ordering based on the underlying Gregorian `date` or JDN for consistency.

### `KurdishDateTime` (optional phase-2)

- Wraps `datetime.datetime` plus Kurdish calendar projection for the date part; delegates all time fields to `datetime`.

### Locales

- Separate **script** (Arabic, Latin, etc.) from **dialect** (Kurmanji, Sorani, Hawrami, …).
- Month and weekday tables live in data modules; no user-controlled format strings executed as code (formatting uses safe templates or `str.format` with fixed keys only).

## Error handling

- **`PyrojRangeError`**: day out of range for month, invalid month, impossible Persian/Islamic date.
- **`PyrojValueError`**: inconsistent parameters, unsupported era combination.
- All public functions document which exceptions they raise.

## Logging

- Use `logging.getLogger(__name__)`.
- Log levels: DEBUG for conversion steps (optional), INFO for library init, WARNING/ERROR for recoverable vs fatal issues.
- Never log environment variables, tokens, or paths from user home unless explicitly part of a debug feature behind a flag.

## Security

- Validate all integer inputs (ranges, types).
- No `pickle` for user data; if serialization is added later, use explicit JSON schema or similar.
- Format strings for user-facing output must not evaluate arbitrary expressions.

## Testing strategy

- **Golden tests**: Known Gregorian ↔ Persian ↔ Kurdish ↔ Islamic tuples from `KurdishDate` tests and `kurdish-calendar.py` samples.
- **Property tests** (optional, `hypothesis` in dev deps only): invariants such as round-trip `gregorian -> jdn -> gregorian`.
- **Edge cases**: Persian leap years (mod 128), Islamic year boundaries, Kurdish month 12 length (29/30).

## References in this repo

- `../KurdishDate/src/dateConverter.ts` — JDN hub, Persian/Islamic/Gregorian.
- `../kurdish-calendar/kurdish-calendar.py` — Emacs-ported calendar, Kurdish ↔ Persian offset.
- Legacy `pyroj/pyroj/rojjmer.py` — to be superseded; depended on `persiantools`.
