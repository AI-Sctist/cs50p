import random
import sys


def get_pnumber(text):
    """
    A function to keep prompting user until it gets a positive number.
    It also make sure that the answer is a number.
    """
    while True:
        try:
            number = int(input(text))
        except ValueError:
            continue

        if number > 0:
            return number


def main():
    """Random a number between 1 and n(user's choice) and let user guess."""

    # Get a valid level (positive number)
    level = get_pnumber("Level: ")

    # Randomly choose a number
    number = random.randint(1, level)

    while True:
        guess = get_pnumber("Guess: ")

        if guess < number:
            print("Too small!")
        elif guess > number:
            print("Too large!")
        else:
            sys.exit("Just right!")


if __name__ == "__main__":
    main()
