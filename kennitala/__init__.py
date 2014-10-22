"""Icelandic national registry codes made easy"""
import re
import random
from datetime import date, timedelta

__author__ = 'Jakub Owczarski'
__version__ = '0.1.1'
__license__ = 'MIT'


class Kennitala:
    """Icelandic national registry codes made easy"""
    def __init__(self, kennitala):
        self.kennitala = kennitala

    class Invalid(Exception):
        """Kennitala is not valid"""

    @staticmethod
    def _get_date(year, month, day):
        """Returns date or raises ValueError"""
        return date(year, month, day)

    @staticmethod
    def _compute_checkdigit(kennitala):
        """Computes checkdigit for (not necessarily complete) kennitala"""
        multipliers = (3, 2, 7, 6, 5, 4, 3, 2)
        summed = 0
        for idx, multiplier in enumerate(multipliers):
            summed += multiplier * int(kennitala[idx])

        checkdigit = 11 - ((summed % 11) or 11)
        return str(checkdigit)

    def _extract_date_parts(self):
        """Returns year, month and day from the kennitala"""
        millenium = '19' if self.kennitala[-1] == '9' else '20'

        day = int(self.kennitala[:2])
        month = int(self.kennitala[2:4])
        year = int(millenium + self.kennitala[4:6])

        return year, month, day

    @staticmethod
    def generate(birth_date):
        """Returns valid kennitala for a given birth_date"""
        full_year = str(birth_date.year)
        year = full_year[-2:]
        millenium = '0' if full_year[0] == '2' else '9'
        month = str(birth_date.month).rjust(2, '0')
        day = str(birth_date.day).rjust(2, '0')
        rnd = str(random.randint(20, 99))

        kennitala = day + month + year + rnd
        checkdigit = Kennitala._compute_checkdigit(kennitala)

        return kennitala + checkdigit + millenium

    @staticmethod
    def random(start=None, end=None):
        """Generate random kennitala for given date range.
        Default range is [1900-01-01, today] inclusive.
        This is pretty memory intensive for large ranges.
        """
        start = start or date(1900, 1, 1)
        end = end or date.today()

        if start > end:
            raise ValueError('Start must not be > end')
        if start == end:
            return Kennitala.generate(start)
        days = (end - start).days
        all_dates = [start + timedelta(days=x) for x in range(days+1)]
        birth_date = random.choice(all_dates)
        return Kennitala.generate(birth_date)

    @staticmethod
    def is_valid(kennitala):
        """Returns True if kenntiala is valid, False otherwise"""
        return Kennitala(kennitala).validate()

    @staticmethod
    def to_date(kennitala):
        """Returns birth date or raises Kennitala.Invalid"""
        return Kennitala(kennitala).get_birth_date()

    def validate(self):
        """Returns True if kennitala is valid, False otherwise"""
        pattern = r'\d{6}\-?\d{4}'
        if not re.match(pattern, self.kennitala):
            return False

        kennitala = self.kennitala.replace('-', '')

        if not kennitala[-1] in ('0', '9'):
            return False

        year, month, day = self._extract_date_parts()

        try:
            Kennitala._get_date(year, month, day)
        except ValueError:
            return False

        checkdigit = Kennitala._compute_checkdigit(kennitala)
        return kennitala[8] == checkdigit

    def get_birth_date(self):
        """Return birth date or raise Kennitala.Invalid"""
        if not self.validate():
            raise Kennitala.Invalid()

        year, month, day = self._extract_date_parts()
        return Kennitala._get_date(year, month, day)
