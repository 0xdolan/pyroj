# Pyroj Calculation Methods & Kurdish Date Academic Research

This document describes how Pyroj computes date conversions at a mathematical level. It also serves as a comprehensive, accurate research reference for academics and historians seeking to understand the mechanics and origins of the **Kurdish Solar Calendar**.

## 1. Calendrical Background

The Kurdish calendar (`Rojjmêrî Kurdî`) is a highly accurate solar calendar rooted deeply in the agricultural, nomadic, and mountainous lifestyles of ancient Kurdistan.

Historically, evidence from the Zagros Mountains indicates that the ancestors of Kurdish populations were among the earliest societies to transition to village-based agriculture. This required an accurate solar year to track seasonal bipartite (summer/winter) divisions, harvest times, and animal mating seasons. Consequently, the names and divisions of the Kurdish months align perfectly with nature.

### 1.1 The Epoch (Year 1)
The calendar requires an anchoring epoch to denote Year 1. There are two prominent historical anchor points recognized in Kurdish history:

1. **The Fall of Nineveh (612 BC)**: This epoch marks the year the Median Empire joined forces with Babylon to defeat the Neo-Assyrian Empire at Nineveh. If using this epoch, one adds `611` (or `612` depending on year zero counting) to the current Gregorian year prior to Newroz.
2. **The Median Empire Baseline (700 BC)**: The classical, widely utilized reference (popularized by Kurdipedia) sets the founding of the Median Empire near 700 BC. In this standard epoch, **1321 years** are added to the Jalali (Persian) solar year.

`pyroj` supports both of these seamlessly via the `KurdishEra` enum, defaulting to the `1321` offset.

### 1.2 Structure of the Year
The new year starts exactly on the Vernal Equinox (the first day of Spring, traditionally March 20 or 21 in the Gregorian system).

* **Spring:** 
  1. Xakelêwe / Newroz (31 Days)
  2. Gulan (31 Days)
  3. Cozerdan (31 Days)
* **Summer:** 
  4. Pûşper (31 Days)
  5. Gelawêj (31 Days)
  6. Xermanan (31 Days)
* **Autumn:** 
  7. Rezber (30 Days)
  8. Gelarêzan / Xezelwer (30 Days)
  9. Sermawez (30 Days)
* **Winter:** 
  10. Befranbar (30 Days)
  11. Rêbendan (30 Days)
  12. Reşeme (29 Days in standard years, 30 Days in leap years)

In total, the first 6 months have 31 days each, the next 5 have 30 days, and the final month has 29 or 30.

---

## 2. Algorithms and Julian Day Hub

Pyroj currently implements:
- Gregorian calendar (`datetime.date` compatible for year range 1..9999)
- Persian (Jalali) solar calendar
- Tabular Islamic calendar
- Kurdish solar calendar (Persian structure + year offset)

The conversion hub is **Julian Day Number (JDN)**.
To provide precision and mathematical safety, the algorithm does not rely on iterative counting. It utilizes the JDN tracking, originating on January 1, 4713 BC.

### 2.1 Constants and Epochs
Pyroj uses standard absolute epoch constants:
- `GREGORIAN_EPOCH = 1721425.5`
- `PERSIAN_EPOCH = 1948320.5`
- `ISLAMIC_EPOCH = 1948439.5`

The Kurdish solar year offset is:
- `KURDISH_SOLAR_YEAR_OFFSET = 1321`
- `kurdish_year = persian_year + 1321`

---

## 3. Gregorian <-> JDN

### 3.1 Gregorian to JDN
Implementation:
```python
def gregorian_to_jdn(year: int, month: int, day: int) -> float:
    adj = 0 if month <= 2 else (-1 if is_gregorian_leap(year) else -2)
    return (
        (GREGORIAN_EPOCH - 1) + 365 * (year - 1)
        + math.floor((year - 1) / 4) - math.floor((year - 1) / 100)
        + math.floor((year - 1) / 400) + math.floor((367 * month - 362) / 12 + adj + day)
    )
```

### 3.2 JDN to Gregorian
It decomposes elapsed days into 400-year cycles (146097 days), 100-year blocks, 4-year blocks, and single years, reconstructing month/day from day-of-year.

---

## 4. Persian (Jalali) <-> JDN

### 4.1 Leap-year predicate
Implementation:
```python
def is_persian_leap_year(year: int) -> bool:
    return ((((((year - (474 if year >= 0 else 473)) % 2820) + 474) + 38) * 682) % 2816) < 682
```
This is Khayyam's 2820-year cycle arithmetic model.

### 4.2 Persian to JDN
```python
def persian_to_jdn(year: int, month: int, day: int) -> float:
    epbase = year - (474 if year >= 0 else 473)
    epyear = 474 + _mod(epbase, 2820)
    return (
        day + ((month - 1) * 31 if month <= 7 else ((month - 1) * 30 + 6))
        + math.floor((epyear * 682 - 110) / 2816)
        + (epyear - 1) * 365
        + math.floor(epbase / 2820) * 1029983
        + (PERSIAN_EPOCH - 1)
    )
```

---

## 5. Islamic (tabular) <-> JDN
Pyroj uses **tabular Islamic arithmetic**.
```python
def is_islamic_leap_year(year: int) -> bool:
    return ((year * 11) + 14) % 30 < 11

def islamic_to_jdn(year: int, month: int, day: int) -> float:
    return (
        day + math.ceil(29.5 * (month - 1)) + (year - 1) * 354
        + math.floor((3 + 11 * year) / 30) + ISLAMIC_EPOCH - 1
    )
```

---

## 6. Kurdish solar conversion
Using the Gregorian baseline, invert the `JDN` into Jalali tuple, and add the offset.

```python
@classmethod
def from_gregorian(cls, d: date, *, era: KurdishEra = KurdishEra.SOLAR_PERSIAN_OFFSET) -> KurdishDate:
    j = gregorian_to_jdn(d.year, d.month, d.day)
    py, pm, pd = jdn_to_persian(j)
    return cls(py + KURDISH_SOLAR_YEAR_OFFSET, pm, pd, era=era)
```

## 7. Weekday mapping
Pyroj handles two conventions:
- Gregorian display: Monday=0..Sunday=6 (`datetime.date.weekday()`)
- Persian/Kurdish/Islamic display: Saturday-first convention (1..7).
  Calculated seamlessly as `(gregorian_weekday + 2) % 7 + 1`.

## 8. Validation and error contract
Raises `PyrojValueError` or `PyrojRangeError` ensuring limits within `1..9999`.

## 9. Worked examples

**Example A**: Gregorian 2018-04-10  
Expected Conversions:
- Persian: 1397-01-21
- Kurdish: 2718-01-21
- Islamic (tabular): 1439-07-24

These values are fully reproduced and asserted rigidly across the Pytest Suite configurations mapping to historical records perfectly.
