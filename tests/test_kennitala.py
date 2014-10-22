"""Tests for kennitala.Kennitala class"""
from datetime import date

import pytest

from kennitala import Kennitala

valid_kennitalas = (
    '140543-3229',  # kennitala of Icelandic president
    '1203753509',  # kennitala of Icelandic prime minister
)

birth_dates = (date(1943, 5, 14), date(1975, 3, 12))

invalid_kennitalas = (
    '1234567890',
    '1503-760649',
    '2513760649',
    '0503760648',
    '550376',
    '1405433219',
)


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_kennitala_ok(kt_no):
    """Tests few real kennitala numbers"""
    kennitala = Kennitala(kt_no)
    assert kennitala.validate()
    # test static version
    assert Kennitala.is_valid(kt_no)


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_fail(kt_no):
    """Makes sure invalid kennitala do not validate"""
    kennitala = Kennitala(kt_no)
    assert not kennitala.validate()
    # same with static version
    assert not Kennitala.is_valid(kt_no)


@pytest.mark.parametrize('info', zip(valid_kennitalas, birth_dates))
def test_kennitala_birth_date(info):
    """Validates birth date extraction"""
    kt_no, birth_date = info
    kennitala = Kennitala(kt_no)
    assert kennitala.get_birth_date() == birth_date
    # same for static version
    assert Kennitala.to_date(kt_no) == birth_date


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_birth_date_raises(kt_no):
    """Tests birth date extraction fails for invalid kennitala"""
    kennitala = Kennitala(kt_no)
    with pytest.raises(Kennitala.Invalid):
        birth_date = kennitala.get_birth_date()
    # same for static version
    with pytest.raises(Kennitala.Invalid):
        birth_date = Kennitala.to_date(kt_no)


def test_kennitala_generate():
    """Tests kennitala generation"""
    today = date.today()
    kt_no = Kennitala.generate(today)
    kennitala = Kennitala(kt_no)
    assert kennitala.validate()
    assert kennitala.get_birth_date() == today


def test_kennitala_random():
    """Tests random kennitala"""
    kt_no = Kennitala.random()
    kennitala = Kennitala(kt_no)
    assert kennitala.validate()
    birth_date = kennitala.get_birth_date()
    assert date(1900, 1, 1) <= birth_date <= date.today()


def test_kennitala_random_invalid_input():
    """Tests that random kennitala fails on invalid input"""
    y2k = date(2000, 1, 1)
    today = date.today()
    with pytest.raises(ValueError):
        kt_no = Kennitala.random(today, y2k)


def test_kennitala_random_same_day():
    """Tests random kennitala"""
    y2k = date(2000, 1, 1)
    kt_no = Kennitala.random(y2k, y2k)
    assert Kennitala.is_valid(kt_no)
    assert Kennitala.to_date(kt_no) == y2k
