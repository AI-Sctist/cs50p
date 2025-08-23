# Practice thinking test-driven development

from datetime import date

from seasons import calculate_age


def test_calculate_age():
    time_delta = date.today() - date(2008, 6, 27)
    assert calculate_age(date(2008, 6, 27)) == round(
        time_delta.days * 1440 + time_delta.seconds / 60
    )
