from plates import is_valid

# Attention!!!
# Each tests must be independable, means that cases in each test only fail in that
# test and pass other tests


def test_isvalid_two_leading_letters():
    assert is_valid("AB") == True
    assert is_valid("A1") == False
    assert is_valid("11") == False


def test_isvalid_length_limit():
    assert is_valid("A") == False
    assert is_valid("AA") == True
    assert is_valid("AAAAAA") == True
    assert is_valid("AAAAAAA") == False


def test_isvalid_numbers_position():
    assert is_valid("ABCD12") == True
    assert is_valid("AB12CD") == False


def test_isvalid_leading_zero():
    assert is_valid("ABCD01") == False


def test_isvalid_periods():
    assert is_valid("AB CDE") == False
    assert is_valid("ABCDE ") == False


def test_isvalid_punctuation():
    assert is_valid("ABCDE.") == False
    assert is_valid("ABCDE!") == False
    assert is_valid("ABCDE?") == False
