# Pyroj Calculation Methods

This document describes how Pyroj computes date conversions at a mathematical level.
It is intended for maintainers and researchers who want reproducible formulas,
algorithm rationale, and worked examples.

## 1) Scope and model

Pyroj currently implements:

- Gregorian calendar (`datetime.date` compatible for year range 1..9999)
- Persian (Jalali) solar calendar
- Tabular Islamic calendar (arithmetical, not moon-sighting based)
- Kurdish solar calendar (Persian structure + year offset)

Core implementation is in:

- `pyroj/_core/convert.py`
- `pyroj/kurdish.py`

The conversion hub is **Julian Day Number (JDN)**.

## 2) Constants and epochs

Pyroj uses the same epoch constants as the TypeScript KurdishDate reference:

- `GREGORIAN_EPOCH = 1721425.5`
- `PERSIAN_EPOCH = 1948320.5`
- `ISLAMIC_EPOCH = 1948439.5`

The Kurdish solar year offset is:

- `KURDISH_SOLAR_YEAR_OFFSET = 1321`

So:

- `kurdish_year = persian_year + 1321`
- `persian_year = kurdish_year - 1321`

## 3) Gregorian <-> JDN

### 3.1 Gregorian to JDN

Implementation:

```29:39:pyroj/_core/convert.py
def gregorian_to_jdn(year: int, month: int, day: int) -> float:
    ...
    adj = 0 if month <= 2 else (-1 if is_gregorian_leap(year) else -2)
    return (
        (GREGORIAN_EPOCH - 1)
        + 365 * (year - 1)
        + math.floor((year - 1) / 4)
        + (-math.floor((year - 1) / 100))
        + math.floor((year - 1) / 400)
        + math.floor((367 * month - 362) / 12 + adj + day)
    )
```

This is the standard arithmetic Gregorian formula:

- Leap years: divisible by 4, except divisible by 100 unless divisible by 400.
- `adj` corrects month-day accumulation after February.

### 3.2 JDN to Gregorian

Implementation:

```42:63:pyroj/_core/convert.py
def jdn_to_gregorian(jdn: float) -> tuple[int, int, int]:
    wjd = math.floor(jdn - 0.5) + 0.5
    depoch = wjd - GREGORIAN_EPOCH
    quadricent = math.floor(depoch / 146097)
    dqc = _mod(depoch, 146097)
    cent = math.floor(dqc / 36524)
    dcent = _mod(dqc, 36524)
    quad = math.floor(dcent / 1461)
    dquad = _mod(dcent, 1461)
    yindex = math.floor(dquad / 365)
    ...
```

It decomposes elapsed days into:

- 400-year cycles (146097 days)
- 100-year blocks
- 4-year blocks
- single years

then reconstructs month/day from day-of-year.

## 4) Persian (Jalali) <-> JDN

### 4.1 Leap-year predicate

Implementation:

```66:68:pyroj/_core/convert.py
def is_persian_leap_year(year: int) -> bool:
    return ((((((year - (474 if year >= 0 else 473)) % 2820) + 474) + 38) * 682) % 2816) < 682
```

This is the 2820-year cycle arithmetic model used in many Jalali algorithmic libraries.

### 4.2 Persian to JDN

Implementation:

```124:141:pyroj/_core/convert.py
def persian_to_jdn(year: int, month: int, day: int) -> float:
    ...
    epbase = year - (474 if year >= 0 else 473)
    epyear = 474 + _mod(epbase, 2820)
    return (
        day
        + ((month - 1) * 31 if month <= 7 else ((month - 1) * 30 + 6))
        + math.floor((epyear * 682 - 110) / 2816)
        + (epyear - 1) * 365
        + math.floor(epbase / 2820) * 1029983
        + (PERSIAN_EPOCH - 1)
    )
```

Key points:

- Months 1..6 have 31 days, 7..11 have 30, month 12 is 29/30.
- Leap correction appears in `floor((epyear * 682 - 110) / 2816)`.

### 4.3 JDN to Persian

Implementation:

```144:165:pyroj/_core/convert.py
def jdn_to_persian(jdn: float) -> tuple[int, int, int]:
    ...
    depoch = jdn - persian_to_jdn(475, 1, 1)
    cycle = math.floor(depoch / 1029983)
    cyear = _mod(depoch, 1029983)
    ...
```

The algorithm inverts `persian_to_jdn` by reconstructing cycle/year/day-of-year.

## 5) Islamic (tabular) <-> JDN

Pyroj uses **tabular Islamic arithmetic** (fixed month-length pattern + leap cycle).
This is deterministic and testable, but it can differ from observational calendars.

### 5.1 Leap-year predicate

```168:172:pyroj/_core/convert.py
def is_islamic_leap_year(year: int) -> bool:
    return ((year * 11) + 14) % 30 < 11
```

### 5.2 Islamic to JDN

```175:196:pyroj/_core/convert.py
def islamic_to_jdn(year: int, month: int, day: int) -> float:
    ...
    return (
        day
        + math.ceil(29.5 * (month - 1))
        + (year - 1) * 354
        + math.floor((3 + 11 * year) / 30)
        + ISLAMIC_EPOCH
        - 1
    )
```

### 5.3 JDN to Islamic

```199:207:pyroj/_core/convert.py
def jdn_to_islamic(jdn: float) -> tuple[int, int, int]:
    ...
    year = int(math.floor((30 * (jdn - ISLAMIC_EPOCH) + 10646) / 10631))
    month = min(12, int(math.ceil((jdn - (29 + islamic_to_jdn(year, 1, 1))) / 29.5) + 1))
    day = int(jdn - islamic_to_jdn(year, month, 1) + 1)
```

## 6) Kurdish solar conversion

Kurdish solar date is defined as:

- same month/day structure as Persian (Jalali)
- Kurdish year = Persian year + 1321

Implementation example:

```68:75:pyroj/kurdish.py
@classmethod
def from_gregorian(cls, d: date, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET) -> KurdishDate:
    j = gregorian_to_jdn(d.year, d.month, d.day)
    py, pm, pd = jdn_to_persian(j)
    return cls(py + KURDISH_SOLAR_YEAR_OFFSET, pm, pd, era=era)
```

## 7) Weekday mapping

Pyroj uses two weekday schemes:

- Gregorian display: Monday=0..Sunday=6 (`datetime.date.weekday()`)
- Persian/Kurdish/Islamic display: Saturday-first convention (1..7 in public helper)

Mapping implementation:

```229:238:pyroj/_core/convert.py
def gregorian_weekday_to_persian_weekday(js_weekday: int) -> int:
    js_weekday = _require_int("js_weekday", js_weekday)
    if js_weekday < 0 or js_weekday > 6:
        raise PyrojRangeError("js_weekday must be in 0..6")
    if js_weekday + 2 == 8:
        return 1
    if js_weekday + 2 == 7:
        return 7
    return js_weekday + 2
```

## 8) Validation and error contract

Public conversion paths enforce:

- `int` only for year/month/day parameters (bool rejected)
- finite numbers for JDN input
- year range `1..9999`
- calendar month/day validity

Errors:

- `PyrojValueError`: wrong type/shape (e.g., bool for year)
- `PyrojRangeError`: out-of-range value (month/day/year)

## 9) Worked examples

## Example A — Gregorian 2018-04-10

Input:

- Gregorian: 2018-04-10

Expected (validated in tests):

- Persian: 1397-01-21
- Kurdish: 2718-01-21
- Islamic (tabular): 1439-07-24

Reference test:

```24:33:tests/test_convert.py
def test_kurdish_date_golden_april_10_2018() -> None:
    d = date(2018, 4, 10)
    j = gregorian_to_jdn(d.year, d.month, d.day)
    assert jdn_to_persian(j) == (1397, 1, 21)
    assert jdn_to_islamic(j) == (1439, 7, 24)
    assert 1397 + 1321 == 2718
```

## Example B — Kurdish to Gregorian

Input:

- Kurdish: 2718-01-21

Procedure:

1. Persian year = 2718 - 1321 = 1397
2. Convert Persian (1397-01-21) -> JDN
3. Convert JDN -> Gregorian

Result:

- Gregorian: 2018-04-10

## Example C — Validation failure

Input:

- `gregorian_to_jdn(True, 1, 1)`

Result:

- raises `PyrojValueError` because bool is not accepted as int.

Reference:

```50:58:tests/test_convert.py
def test_convert_rejects_bool_and_ranges() -> None:
    with pytest.raises(PyrojValueError):
        gregorian_to_jdn(True, 1, 1)
```

## 10) Reproducibility and caveats

- All formulas are deterministic for the supported range.
- Islamic results are tabular, not observational.
- Current public API is date-level; full datetime/fractional-day API is planned.
- Locale strings come from `pyroj/locales/catalog.json`; numeric conversion logic is independent from locale labels.
