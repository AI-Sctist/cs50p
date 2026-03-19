from pytest import raises

from working import convert


def test_convert_incorrect_pattern():
    with raises(ValueError):
        convert("i work from 8:00 AM to 8:01 AM")


def test_convert_missing_to():
    with raises(ValueError):
        convert("10 AM 10 PM")


def test_convert_missing_time():
    with raises(ValueError):
        convert(" to ")


def test_convert_missing_meridiem():
    with raises(ValueError):
        convert("10 to 11")


def test_convert_not_numeric():
    with raises(ValueError):
        convert("AC:00 AM to AB:00 PM")
        convert("13:AC AM to 13:PM PM")


def test_convert_invalid_time():
    with raises(ValueError):
        convert("13:00 AM to 10:00 PM")
        convert("10:60 AM to 10:00 PM")
        convert("24:00 PM to 10:00 PM")


def test_convert_full_input():
    assert convert("9:00 AM to 9:00 PM") == "09:00 to 21:00"
    assert convert("9:00 PM to 9:00 AM") == "21:00 to 09:00"


def test_convert_shorter_input():
    assert convert("9 AM to 9 PM") == "09:00 to 21:00"
    assert convert("9 AM to 9:00 PM") == "09:00 to 21:00"
    assert convert("9:00 AM to 9 PM") == "09:00 to 21:00"
