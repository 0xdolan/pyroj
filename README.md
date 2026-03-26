# pyroj (Kurdish Calendar)

**pyroj** is the definitive Python library for the Kurdish **solar** calendar. It allows for highly accurate date conversions to and from **Gregorian**, **Persian (Jalali)**, and **Tabular Islamic** dates. 

Built exclusively under the Python standard library, it inherits natively from Python's own `datetime` ecosystem, serving as a dynamic, robust drop-in replacement for any application. **Runtime dependencies: none.**

- **Python**: 3.10+
- **Dependency/tool workflow**: `uv` + `pyproject.toml`
- **Supported year range**: `1..9999` (aligned with Python `datetime.date`)

> **[Research Reference & Calculation Details]**  
> For academics, developers, and researchers seeking the complete historical methodology, epoch derivations, and algorithmic calculations used to yield accurate Kurdish dates, please refer to the detailed [Kurdish Date Calculation Research](docs/CALCULATION_METHODS.md).

## Quick Start

`KurdishDate` and `KurdishDateTime` inherit natively from python's built-in `datetime.date` and `datetime.datetime`. Any standard operation you perform on Python dates can be seamlessly performed on Kurdish dates!

```bash
uv pip install pyroj
# or
pip install pyroj
```

## Documentation Index

- [Architecture](docs/ARCHITECTURE.md)
- [Calculation Methods](docs/CALCULATION_METHODS.md)
- [Locale Reference (full tables and mappings)](docs/LOCALES.md)

### Basic Creation and Conversions
```python
from datetime import date
from pyroj.kurdish import KurdishDate

# 1. Start from a Gregorian Date
d = date(2026, 3, 23)
kd = KurdishDate.from_gregorian(d)

print(kd.year, kd.month, kd.day)  # Output: 2726 1 3

# 2. Or initialize natively in Kurdish
kd_native = KurdishDate(2726, 1, 3)

# 3. Effortless Conversions to other systems
print(kd.to_gregorian())          # Output: 2026-03-23
print(kd.to_persian())            # Output: (1405, 1, 3)
print(kd.to_islamic())            # Output: (1447, 10, 4)
```

### Advanced Date Mathematics
Because `pyroj` extends standard lib classes natively, you can rely on robust Python implementations for adding/subtracting ranges without worrying about leap years or skipped months!

```python
from datetime import timedelta
from pyroj.kurdish import KurdishDateTime

# Adding 5 days over month boundaries calculates correctly
kd = KurdishDate(2726, 1, 30)
kd_new = kd + timedelta(days=5)

print(kd_new)  # Output: 2726-02-04

# Full Time/Datetime wrappers exist
kdt = KurdishDateTime(2726, 1, 3, hour=15, minute=30, second=0)

kdt_shuffled = kdt - timedelta(hours=36)
print(kdt_shuffled) # Output: 2726-01-02 03:30:00
```

## Beautiful Native Formatting (`strftime`)

Formatting strings out of the box matches Python's `%` standard exactly. Furthermore, `pyroj` natively maps out month and weekday translations depending on your selected locale.

Supported `LocaleId` dialects include `KMR` (Kurmanji / Kurdish-Latin script), `CKB` (Sorani / Kurdish-Arabic script), compatibility alias `KU` (maps to `CKB`), plus `AR` (Arabic), `FA` (Persian), `TR` (Turkish), and `EN` (English). Additional ISO aliases are resolved dynamically: `sdh`, `lki`, `hac` -> `CKB`, and `zza` (`diq`/`kiu`) -> `KMR`.

```python
from pyroj.kurdish import KurdishDate
from pyroj.locales import LocaleId

kd = KurdishDate(2726, 1, 25)

# Standard English representation
print(kd.strftime("%A, %d %B %Y", locale=LocaleId.EN))
# Output: Tuesday, 25 Xakelêwe 2726

# Sorani execution (Arabic-script Kurdish)
print(kd.strftime("%A, %d %B %Y", locale=LocaleId.CKB))
# Output: سێشەممە, 25 خاکەلێوە 2726

# Kurmanji execution (Latin-script Kurdish)
print(kd.strftime("%A, %d %B %Y", locale=LocaleId.KMR))
# Output: Tuesday, 25 Xakelêwe 2726

# Persian representation
print(kd.strftime("%A, %d %B %Y", locale=LocaleId.FA))
# Output: سه‌شنبه, 25 خاکِ‌لِیوَه 2726

# Available formats: 
# %Y (4-digit Year), %y (2-digit Year)
# %B (Full Month), %b (Short Month), %m (2-digit Month), %-m (1-digit Month)
# %A (Full Weekday), %a (Short Weekday), %w (1-7 Index), %-w (1-7 Number)
# %d (2-digit Day), %-d (1-digit Day)
# %H:%M:%S etc. for KurdishDateTime.
```

String locale negotiation is also supported dynamically:

```python
print(kd.strftime("%B %Y", locale="kmr"))      # Kurmanji
print(kd.strftime("%B %Y", locale="ckb"))      # Sorani
print(kd.strftime("%B %Y", locale="ku"))       # Backward-compat alias -> CKB
```

You can also switch Kurdish month-name variants dynamically:

```python
from pyroj import CalendarKind, format_calendar_date

print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="ckb", kurdish_variant="standard"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr", kurdish_variant="gelarêzan"))
```

For months that have multiple accepted names in a dialect table, `pyroj` preserves the canonical combined form from the source (for example, `Nîsanê/Lîzan` or `نیسانە/لیزان`) and returns it as-is when that variant is selected.

### Complete Locale Tables and Detailed Mapping

For full per-dialect markdown tables (canonical names, aliases, month variants, and examples), see:

- [Locale Reference](docs/LOCALES.md)

### Sorani and Kurmanci (Detailed Formatting)

Kurdish Sorani (`ckb`) uses the Arabic script, and Kurmanci (`kmr`) uses the Latin script. The default month names for the first month (starting in March) are "خاکه‌لێوه" (Xakelêwe) and "Nîsan", but **"نەورۆز" (Newroz)** is widely used as a second alternative!

```python
from datetime import date
from pyroj import CalendarKind, KurdishDate, LocaleId, format_calendar_date, get_locale

# March 22nd is Kurdish Month 1, Day 2
kd = KurdishDate.from_gregorian(date(2026, 3, 22)) 

# Full Month (%B) and Full Weekday (%A) in Sorani (CKB)
print(format_calendar_date(kd, "%A, %d %B %Y", calendar=CalendarKind.KURDISH, locale=LocaleId.CKB))
# Output: یەکشەممە, 02 خاکه‌لێوه 2726

# Full Month (%B) and Full Weekday (%A) in Kurmanci (KMR)
print(format_calendar_date(kd, "%A, %d %B %Y", calendar=CalendarKind.KURDISH, locale=LocaleId.KMR))
# Output: Yekşem, 02 Nîsan 2726

# Short Weekday (%a) and Short Month (%b) in Sorani
print(format_calendar_date(kd, "%a, %d %b %Y", calendar=CalendarKind.KURDISH, locale=LocaleId.CKB))
# Output: یەک, 02 خاک 2726

# Short Weekday (%a) and Short Month (%b) in Kurmanci
print(format_calendar_date(kd, "%a, %d %b %Y", calendar=CalendarKind.KURDISH, locale=LocaleId.KMR))
# Output: Yek, 02 Nîs 2726

# Accessing the first vs second name options for March (Month 1) directly from the locale cache
ckb_months = get_locale(LocaleId.CKB).names(CalendarKind.KURDISH).months
kmr_months = get_locale(LocaleId.KMR).names(CalendarKind.KURDISH).months

# Default First Name (Index 0)
print(ckb_months[0][0])  # Output: خاکه‌لێوه
print(kmr_months[0][0])  # Output: Nîsan

# Alternative Second Name (Index 1) - Newroz
print(ckb_months[0][1])  # Output: نەورۆز
print(kmr_months[0][1])  # Output: Newroz
```

### Other Kurdish Dialect Variants

You can dynamically switch Kurdish month-name variants to format dates in other standard dialects.

```python
from pyroj import CalendarKind, format_calendar_date

# Syriac (KMR)
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr", kurdish_variant="syriac"))

# Laki
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="lki", kurdish_variant="lki_laki"))

# Hawrami / Gorani
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="hac", kurdish_variant="hac_hawrami"))

# Kalhuri / Southern Kurdish
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="sdh", kurdish_variant="sdh_kelhuri"))

# Zazaki
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="zza", kurdish_variant="zza_zazaki"))
```

### Gregorian, Persian, Arabic, and Turkish Formatting

Because `pyroj` operates dynamically, you can freely convert your initialized `KurdishDate` into Gregorian, Persian, or Islamic tuples, and format them directly into Persian, Arabic, and Turkish native text locales.

```python
from datetime import date
from pyroj import CalendarKind, KurdishDate, LocaleId, format_calendar_date

kd = KurdishDate(2726, 1, 1) # March 21, 2026

# Point Conversions
print(kd.to_gregorian()) # Output: 2026-03-21
print(kd.to_persian())   # Output: (1405, 1, 1)
print(kd.to_islamic())   # Output: (1447, 10, 2)

# Formatting in Persian Native Locale
print(format_calendar_date(kd, "%A, %d %B", calendar=CalendarKind.PERSIAN, locale=LocaleId.FA))
# Output: شنبه, 01 فروردین

# Formatting in Arabic Native Locale 
print(format_calendar_date(kd, "%A, %d %B", calendar=CalendarKind.ISLAMIC, locale=LocaleId.AR))
# Output: السبت, 02 شوّال

# Formatting Gregorian in Turkish Locale
print(format_calendar_date(kd, "%A, %d %B %Y", calendar=CalendarKind.GREGORIAN, locale=LocaleId.TR))
# Output: Cumartesi, 21 Mart 2026
```

### Detailed DateTime Locale Example

```python
from pyroj import KurdishDateTime

kdt = KurdishDateTime(2726, 1, 4, hour=15, minute=10, second=0)

# Locale-aware AM/PM
print(kdt.strftime("%Y-%m-%d %I:%M %p", locale="ckb"))
print(kdt.strftime("%Y-%m-%d %I:%M %p", locale="kmr"))
```

## Historical Eras

Historically, different subsets of researchers align `Year 1` of the Kurdish Calendar differently. `pyroj` accommodates this dynamically via the `KurdishEra` Enum:

1. **Median Empire Baseline** `SOLAR_PERSIAN_OFFSET` (Default): Evaluates the standard Kurdipedia offset where `Kurdish Year = Jalali Year + 1321`. (Anchored near 700 BC).
2. **Fall of Nineveh Epoch** `FALL_OF_NINEVEH`: Tracks the exact 612 BC battle of Nineveh where `Kurdish Year = Jalali Year + 1233`.

```python
from pyroj.kurdish import KurdishDate, KurdishEra

# Calculates the year offset depending on standard
kd_nineveh = KurdishDate(2638, 1, 3, era=KurdishEra.FALL_OF_NINEVEH)
print(kd_nineveh.to_gregorian()) # Extrapolates out correctly
```

## Native Tooling (JDN Helpers & Timestamps)

You can convert any Gregorian or Julian representation efficiently down into `int` / `float` structs.

```python
from pyroj._core.convert import gregorian_datetime_to_jdn, jdn_to_gregorian_datetime
from pyroj.kurdish import KurdishDate

# Extract absolute Julian Day Number directly
kd = KurdishDate(2726, 1, 1)
print(kd.to_jdn())  # Returns Absolute JDN float

# Restore from JDN
kd_restored = KurdishDate.from_jdn(2461122.5)
```

## Development setup (uv + ruff)

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check pyroj tests
uv run mypy pyroj
```

Install the package locally for development:

```bash
uv pip install -e .
```

## Continuous integration
GitHub Actions runs **pytest**, **ruff**, and **mypy** on Python 3.10–3.13 (see `.github/workflows/ci.yml`).

## License
GPL.
