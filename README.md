
# Rojjmer (Kurdish Calendar)

Welcome to **Rojjmer (Kurdish Calendar)** - a small **_Python_** library for converting Gregorian and Solar dates to Kurdish date and vice versa.

## Installation

  How to install the module:

  `pip install pyroj`

  for python 3 in Linux:

  `pip3 install pyroj`

  or

  `python3 -m pip install pyroj`

  Install the package using the setup.py script:
  First cd into the root directory where setup.py is located, then install via below command:

  `python setup.py install`

  **Need help on installing Python modules, click on below link:**

- [How to install Python modules](https://docs.python.org/3.9/installing/index.html)

---

## How to use Kurdish calendar

### Get the Kurdish date

```python
from pyroj import rojjmer

# make an instance from the class with Gregorian date
CAL = rojjmer.Rojjmer(2020, 12, 28)
print(CAL.to_kurdish(solar=False))

# Output:
# 2720-10-08

# make an instance from the class with Solar date
CAL = rojjmer.Rojjmer(1399, 10, 8)
print(CAL.to_kurdish(solar=True))

# Output:
# 2720-10-08
```

### Get the Kurdish date - Only year, month or day

```python
from pyroj import rojjmer

# make an instance from the class with Gregorian date
CAL = rojjmer.Rojjmer(2020, 12, 28)

# Get only the year
print("YEAR:", CAL.to_kurdish().year)

# Get only the month
print("MONTH:", CAL.to_kurdish().month)

# Get only the day
print("DAY:", CAL.to_kurdish().day)

# Output:
# YEAR: 2720
# MONTH: 10
# DAY: 8
```

### Get the Kurdish Weekday (in Arabic-based and Latin-based)

```python
from pyroj import rojjmer

# make an instance from the class with Gregorian date
CAL = rojjmer.Rojjmer(2020, 12, 28)

print("WEEKDAY:", CAL.hefte())
# Output:
# WEEKDAY: دووشەممە

print("WEEKDAY:", CAL.hefte(abbr=False, latin=False))
# Output:
# WEEKDAY: دووشەممە


print("Abbreviated WEEKDAY:", CAL.hefte(abbr=True, latin=False))
# Output:
# Abbreviated WEEKDAY: د


print("Abbreviated WEEKDAY:", CAL.hefte(abbr=True, latin=True))
# Output:
# Abbreviated WEEKDAY: D


print("WEEKDAY:", CAL.hefte(abbr=False, latin=True))
# Output:
# WEEKDAY: Dûşemme

```

### Get the Kurdish Month Names (in Arabic-based and Latin-based)

```python

# make an instance from the class with Gregorian date
CAL = rojjmer.Rojjmer(2021, 3, 21)

print("Month Name:", CAL.month_name())
# Output:
# Month Name: خاکەلێوە

# Those months have two names, will be accessible via second_name parameter to be True
print("Month Name (second name):", CAL.month_name(second_name=True))
# Output:
# Month Name: نەورۆز

print("Month Name:", CAL.month_name(second_name=False, latin=True))
# Output:
# Month Name: Xakelêwe

# Those months have two names, will be accessible via second_name parameter to be True
print("Month Name (second name):", CAL.month_name(second_name=True, latin=True))
# Output:
# Month Name: Newroz

```

## To-Do List

- N/A

---

## Getting help

If you have questions about the python library **Kurdish calendar** module, or run into problems, or if you want to contribute in any way, feel free to reach out to me via below links:

- **[GitHub](https://github.com/dolanskurd)**
- **[PyPI](https://pypi.org/project/kurdish-calendar/)**
- **[Twitter](http://www.twitter.com/dolanskurd)**
- **E-mail: [dolanskurd@mail.com](mailto:dolanskurd@mail.com)**

## Donate

If you think it deserves, **DONATE**:

- **[iTunes Gift Cards via PayPal (Email-Delivery)](https://www.paypal.com/us/gifts/brands/itunes)** to my Apple ID: **dolanskurd@gmail.com**

## License

Kurdish Calendar Library is available under the **MIT license**.
