import re
import sys

import datetime
import inflect


def get_birthdate() -> tuple[int, int, int]:
    """
    Get user's birthdate in YYYY-MM-DD format and return date in datetime.date obj
    Exit if the user does not enter date correctly in YYYY-MM-DD format
    """
    date = input("Date of Birth: ")
    if match := re.fullmatch(r"([0-9]{4})-([0-9]{2})-([0-9]{2})", date):
        try:
            birthdate = datetime.date(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        except ValueError:
            sys.exit("Invalid date")
        return birthdate
    else:
        sys.exit("Invalid date")


def calculate_age(birthdate: datetime.date) -> int:
    """Calculate user's age in minutes and round it to the nearest integer."""
    time_delta = datetime.date.today() - birthdate
    return round(time_delta.days * 1440 + time_delta.seconds / 60)


def main() -> None:
    """Tell user how old they are in minutes."""
    user_age = calculate_age(get_birthdate())

    e = inflect.engine()

    minutes = e.number_to_words(user_age, andword="")
    print(minutes.capitalize(), "minutes")


if __name__ == "__main__":
    main()
