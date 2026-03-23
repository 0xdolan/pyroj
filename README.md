# pyroj (Kurdish Calendar)

**pyroj** is a Python library for the Kurdish **solar** calendar and conversions to/from **Gregorian**, **Persian (Jalali)**, and **tabular Islamic** dates. **Runtime dependencies: none** — only the Python standard library (`datetime`, etc.). Calendar math uses the same Julian-day hub as the **KurdishDate** TypeScript reference (see sibling folder in the monorepo) in the Kurdistanica-style model (**Kurdish year = Persian year + 1321**).

- **Python**: 3.10+
- **Install**: `pip install .` or `pip install -e ".[dev]"` for development (pytest, ruff, mypy)

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

- `docs/ARCHITECTURE.md` — eras, JDN hub, security notes
- `docs/REFACTOR_TASKMASTER.json` — task list for larger features (locales, formatting, CI)

## License

MIT.
