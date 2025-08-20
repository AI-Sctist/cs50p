from um import count


def test_count_um_stands_alone():
    assert count("Um") == 1


def test_count_substring():
    assert count("AI-Sctist has an umbrella") == 0


def test_count_comma():
    assert count("Something happens when we, um, haiz") == 1


def test_count_question_mark():
    assert count("Did you know the meaning of the word um?") == 1


def test_count_dot():
    assert count("Um... what are regular expressions?") == 1
