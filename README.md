# pyroj (Kurdish Calendar)

**pyroj** is a Python library for the Kurdish **solar** calendar and conversions to/from **Gregorian**, **Persian (Jalali)**, and **tabular Islamic** dates. **Runtime dependencies: none** — only the Python standard library (`datetime`, etc.). Calendar math uses the same Julian-day hub as the **KurdishDate** TypeScript reference (see sibling folder in the monorepo) in the Kurdistanica-style model (**Kurdish year = Persian year + 1321**).

- **Python**: 3.10+
- **Install**: `pip install .` or `pip install -e ".[dev]"` for development (pytest, ruff, mypy)
- **Supported year range**: `1..9999` for public APIs (aligned with Python `datetime.date`)

## Quick start

```python
from datetime import date
from pyroj import KurdishDate, gregorian_to_islamic, gregorian_to_persian

d = date(2018, 4, 10)
kd = KurdishDate.from_gregorian(d)
print(kd.year, kd.month, kd.day)   # 2718 1 21
print(kd.to_persian())             # (1397, 1, 21)
print(kd.to_islamic())             # (1439, 7, 24)
print(gregorian_to_persian(d))
print(gregorian_to_islamic(d))
```

### `datetime.date`-style usage

`KurdishDate` is an immutable value object: comparison, `hash`, `replace`, and conversion helpers behave like a calendar-specific `date`.

```python
from pyroj import KurdishDate

a = KurdishDate.from_persian(1397, 1, 21)
b = KurdishDate.from_kurdish_solar(2718, 1, 21)
assert a == b
assert a.to_gregorian().isoformat() == "2018-04-10"
```

## Locales and safe formatting

Month and weekday names are available for **English**, **Kurdish (Kurmanji-style Arabic script)**, **Persian (Farsi)**, **Turkish**, and **Arabic**. Gregorian weekday lists use **Monday → Sunday**; Kurdish / Persian / Islamic use **Saturday → Friday** (same indexing as the KurdishDate reference).

Formatting uses **fixed tokens only** (no `str.format` fields, no `{braces}`, no `%` — see `validate_pattern_safe`). Tokens include `YYYY`, `MM`, `DD`, `MMMM`, `MMM`, `dddd`, `ddd`, `dd`, `d`, `WW`.

```python
from datetime import date
from pyroj import (
    CalendarKind,
    KurdishDate,
    LocaleId,
    format_calendar_date,
    format_iso_date,
    get_locale,
    to_locale_digits,
)

kd = KurdishDate.from_gregorian(date(2018, 4, 10))
print(format_iso_date(kd, locale=LocaleId.EN))
print(format_calendar_date(kd, "YYYY MMMM (dddd)", calendar=CalendarKind.KURDISH, locale=LocaleId.KU))
print(to_locale_digits("2718", get_locale(LocaleId.FA)))
```

## Continuous integration

GitHub Actions runs **pytest**, **ruff**, and **mypy** on Python 3.10–3.13 (see `.github/workflows/ci.yml`).

## Locale data

Editable month and weekday strings live in **`pyroj/locales/catalog.json`** (loaded at import). To add or adjust a locale, edit that file and keep the same JSON shape (`locales.<key>.gregorian|persian|kurdish|islamic` plus `digits` and `am_pm`).

## Legacy `Rojjmer`

The previous API remains for compatibility; prefer `KurdishDate` for new code.

```python
from pyroj.rojjmer import Rojjmer

cal = Rojjmer(2018, 4, 10)          # Gregorian
kd = cal.to_kurdish()               # KurdishDate
assert kd.year == 2718

# to_gregorian() treats (year, month, day) as Persian (Jalali), like old JalaliDate(...)
cal2 = Rojjmer(1399, 10, 8)
assert cal2.to_gregorian().isoformat() == "2020-12-28"
```

## Documentation

- `docs/ARCHITECTURE.md` — design overview (eras, JDN hub)
- `docs/CALCULATION_METHODS.md` — full formulas, derivations, and worked examples
- `docs/REFACTOR_TASKMASTER.json` — canonical detailed task roadmap

## License

MIT.
