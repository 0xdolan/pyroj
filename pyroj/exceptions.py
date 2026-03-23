"""Pyroj-specific exceptions."""


class PyrojError(Exception):
    """Base class for all Pyroj errors."""


class PyrojValueError(PyrojError, ValueError):
    """Invalid argument type or inconsistent calendar parameters."""


class PyrojRangeError(PyrojError, ValueError):
    """Date components outside the valid range for the calendar."""
