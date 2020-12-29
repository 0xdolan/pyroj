# -*- coding: utf-8 -*-

from setuptools import setup
from os import path


myPath = path.abspath(path.dirname(__file__))
with open(path.join(myPath, "README.md"), encoding="utf-8") as f:
    README = f.read()

setup(
    name="pyroj",
    version="0.0.2",
    author="Dolan Hêriş",
    author_email="dolanskurd@mail.com",
    url="https://github.com/dolanskurd/pyroj",
    description=("Converting Gregorian and Solar dates to Kurdish date"),
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="kurdish language module library converter calendar date gregorian digits persian farsi latin english kurdi",
    packages=["pyroj"],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Topic :: Documentation",
        "Topic :: Printing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Text Processing :: Fonts",
        "Topic :: Text Editors :: Word Processors",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
