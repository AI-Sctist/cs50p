from numb3rs import validate


def test_validate_correct_ipv4():
    assert validate("1.1.1.1") is True
    assert validate("255.255.255.255") is True


def test_validate_leading_zeroes():
    assert validate("0.0.0.10") is True
    assert validate("00.1.1.1") is False
    assert validate("01.1.1.1") is False


def test_validate_match_pattern():
    assert validate("1.1.1,1") is False
    assert validate("1.1.1.") is False
    assert validate("1.1.1") is False
    assert validate("1.1.1.1.1") is False


def test_validate_value_range():
    assert validate("1.1.1.256") is False


def test_validate_value_error():
    assert validate("cat.dog.1.1") is False
    assert validate("a.b.c.d") is False
    assert validate("*.*.*.*") is False
