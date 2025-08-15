from bank import value


def test_value_0dollars():
    assert value("hello") == 0
    assert value("hello, AI-Sctist") == 0
    assert value("hello, world!") == 0


def test_value_0dollars_case_insensitive():
    assert value("HELLO") == 0
    assert value("HELLO, AI-SCTIST") == 0
    assert value("HELLO, WORLD!") == 0


def test_value_20dollars():
    assert value("hey") == 20
    assert value("hey, AI-Sctist") == 20
    assert value("hey, world!") == 20


def test_value_20dollars_case_insensitive():
    assert value("HEY") == 20
    assert value("HEY, AI-SCTIST") == 20
    assert value("HEY, WORLD!") == 20


def test_value_100dollars():
    assert value("good morning") == 100
    assert value("good morning AI-Sctist") == 100
    assert value("good morning world!") == 100
    assert value("good") == 100


def test_value_100dollars_case_insensitive():
    assert value("GOOD MORNING") == 100
    assert value("GOOD MORNING AI-SCTIST") == 100
    assert value("GOOD MORNING WORLD!") == 100
    assert value("GOOD") == 100
