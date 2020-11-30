
# Kurdish Calendar

Welcome to **Kurdish Calendar** - a small **_Python_** library for converting Gregorian and Solar dates to Kurdish date.

## Installation

  How to install the module:

  `pip install kurdish-calendar`

  for python 3 in Linux:

  `pip3 install kurdish_calendar`

  or

  `python3 -m pip install kurdish-calendar`

  Install the package using the setup.py script:
  First cd into the root directory where setup.py is located, then install via below command:

  `python setup.py install`

  **Need help on installing Python modules, click on below link:**

- [How to install Python modules](https://docs.python.org/3.9/installing/index.html)

---

## How to use Kurdish calendar

### Get the Kurdish date

```python
from kurdish_calendar import calendar_ku

# make an instance from the class with Gregorian date
CAL = calendar_ku.Rojjmer(2020, 11, 30)
print(CAL.ku_date(solar=False))

# Output:
# 2720-09-10

# make an instance from the class with Solar date
CAL = calendar_ku.Rojjmer(1399, 9, 10)
print(CAL.ku_date(solar=True))

# Output:
# 2720-09-10
```

### Get the Kurdish date - Only year, month or day

```python
from kurdish_calendar import calendar_ku

# make an instance from the class with Gregorian date
CAL = calendar_ku.Rojjmer(2020, 11, 30)

# Get only the year
print("YEAR:", CAL.ku_date().year)

# Get only the month
print("MONTH:", CAL.ku_date().month)

# Get only the day
print("DAY:", CAL.ku_date().day)

# Output:
# YEAR: 2720
# MONTH: 9
# DAY: 10
```

### Get the Kurdish weekday

```python
from kurdish_calendar import calendar_ku

# make an instance from the class with Gregorian date
CAL = calendar_ku.Rojjmer(2020, 11, 30)

print("WEEKDAY:", CAL.hefte())
print("Abbreviated WEEKDAY:", CAL.hefte(abbr=True))

# Output:
# WEEKDAY: دووشەممە
# Abbreviated WEEKDAY: د
```

## To-Do List

- N/A

---

## Getting help

If you have questions about the python library **Kurdish calendar** module, or run into problems, or if you want to contribute in any way, feel free to reach out to me via below links:

- **[GitHub](https://github.com/dolanskurd)**
- **[PyPI](https://pypi.org/project/kurdish_calendar/)**
- **[Twitter](http://www.twitter.com/dolanskurd)**
- **E-mail: [dolanskurd@mail.com](mailto:dolanskurd@mail.com)**

## Donate

If you think it deserves, **DONATE**:

- **[iTunes Gift Cards via PayPal (Email-Delivery)](https://www.paypal.com/us/gifts/brands/itunes)** to my Apple ID: **dolanskurd@gmail.com**

## License

Kurdish Calendar Library is available under the **MIT license**.
