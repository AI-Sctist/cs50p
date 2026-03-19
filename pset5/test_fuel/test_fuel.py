import pytest

from fuel import convert
from fuel import gauge

# Attention!!!
# Each tests must be independable, means that cases in each test only fail in that
# test and pass other tests

# My stupid mistake before: forget to check the correctness of the output -_-


def test_convert_non_numeric():
    with pytest.raises(ValueError):
        convert("cat/dog")


def test_convert_nonvalid_percentage():
    with pytest.raises(ValueError):
        convert("100/99")


def test_convert_zero_division():
    with pytest.raises(ZeroDivisionError):
        convert("0/0")


def test_convert_negative_fraction():
    with pytest.raises(ValueError):
        convert("-6/9")

    with pytest.raises(ValueError):
        convert("-9/-6")


def test_convert_incorrect_output():
    assert convert("1/100") == 1
    assert convert("50/100") == 50
    assert convert("99/100") == 99


def test_gauge_less_or_equal_1():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(50) == "50%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"
