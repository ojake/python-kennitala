python-kennitala
================

python-kennitala is a python library for common operations on Icelandic
National Registry codes - [kennitala](https://en.wikipedia.org/wiki/Kennitala).

## Capabilities

* Validation of kennitala
* Extraction of birth date from kennitala
* Generating kennitala for a given birth date
* Generating random kennitala

## Usage

    >>> from kennitala import Kennitala
    >>>
    >>> kt_no = '0101109639'
    >>> kennitala = Kennitala(kt_no)
    >>> kennitala.validate()
    True
    >>> kennitala.get_birth_date()
    datetime.date(1910, 1, 1)
    >>> kennitala = Kennitala(kt_no.replace('3', '4'))
    >>> kennitala.validate()
    False
    >>> kennitala.get_birht_date()
    Traceback (most recent call last):
        File kennitala.py, in get_birth_date
    kennitala.Invalid
    >>>


## Installation

inside your virtualenv execute:

    $ pip install kennitala

or download and install manually.


## Tests

Tests are written for [py.test](https://pytest.org/latest)

To run tests simply execute:

    $ PYTHONPATH=./ py.test tests
