"""Tests for kennitala.Kennitala class"""
from datetime import date

import pytest

from kennitala import Kennitala

valid_kennitalas = (
    '140543-3229',  # kennitala of Icelandic president
    '1203753509',  # kennitala of Icelandic prime minister
    '6503760649',  # kennitala of Þjóðskrá Íslands (Registry Iceland)
)

birth_dates = (date(1943, 5, 14), date(1975, 3, 12))

invalid_kennitalas = (
    '1234567890',
    '1503-760649',
    '2513760649',
    '0503760648',
    '0503760647',
    '550376',
    '1405433219',
    '28129420229',
)


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_str_ok(kt_no):
    kennitala = Kennitala(kt_no)
    assert str(kennitala) == kt_no

@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_str_inv(kt_no):
    kennitala = Kennitala(kt_no)
    assert str(kennitala) == 'Invalid kennitala'


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_kennitala_ok(kt_no):
    """Tests few real kennitala numbers"""
    kennitala = Kennitala(kt_no)
    assert kennitala.validate(), kt_no
    # test static version
    assert Kennitala.is_valid(kt_no), kt_no


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_fail(kt_no):
    """Makes sure invalid kennitala do not validate"""
    kennitala = Kennitala(kt_no)
    assert not kennitala.validate(), kt_no
    # same with static version
    assert not Kennitala.is_valid(kt_no), kt_no


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


@pytest.mark.parametrize('person', (True, False))
@pytest.mark.parametrize('idx', range(100))
def test_kennitala_generate(idx, person):
    """Test bunch of generated kennitalas"""
    today = date.today()
    kt_no = Kennitala.generate(today, person)
    kennitala = Kennitala(kt_no)
    assert kennitala.validate(), kt_no
    assert kennitala.get_birth_date() == today
    assert kennitala.is_person() == person


def test_kennitala_random():
    """Tests random kennitala"""
    kt_no = Kennitala.random()
    kennitala = Kennitala(kt_no)
    assert kennitala.validate(), kt_no
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


def test_kennitala_is_valid_none():
    """Tests that None is not valid kennitala"""
    kennitala = Kennitala(None)
    assert not kennitala.validate()
    assert not Kennitala.is_valid(None)


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_kennitala_is_person(kt_no):
    """Tests kennitala type detection"""
    kennitala = Kennitala(kt_no)
    first_digit = int(kt_no[0])
    personal = (0 <= first_digit <= 3)
    assert kennitala.is_person() == personal
    assert Kennitala.is_personal(kt_no) == personal


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_is_person_fails(kt_no):
    """Tests kennitala type detection"""
    kennitala = Kennitala(kt_no)
    first_digit = int(kt_no[0])
    personal = (0 <= first_digit <= 3)
    with pytest.raises(Kennitala.Invalid):
        fail = kennitala.is_person()


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_only_digits_raises(kt_no):
    """Tests Kennitala.only_digits raises on invalid input"""
    kennitala = Kennitala(kt_no)
    with pytest.raises(Kennitala.Invalid):
        digits = kennitala.only_digits()


@pytest.mark.parametrize('kt_no', invalid_kennitalas)
def test_kennitala_with_dash_raises(kt_no):
    """Tests Kennitala.with_dash raises on invalid input"""
    kennitala = Kennitala(kt_no)
    with pytest.raises(Kennitala.Invalid):
        dashed = kennitala.with_dash()


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_kennitala_only_digits(kt_no):
    """Test kennitala only_digits"""
    kennitala = Kennitala(kt_no)
    digits = kennitala.only_digits()
    assert len(digits) == 10
    assert all(x.isdigit() for x in digits)


@pytest.mark.parametrize('kt_no', valid_kennitalas)
def test_kennitala_with_dash(kt_no):
    """Test kennitala only_digits"""
    kennitala = Kennitala(kt_no)
    dashed = kennitala.with_dash()
    assert len(dashed) == 11
    assert len([x for x in dashed if x.isdigit()]) == 10
    assert dashed.count('-') == 1
    assert dashed[6] == '-'
