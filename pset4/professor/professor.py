import random
import sys

MATH_PROBLEMS = 10
ATTEMPS = 3


def get_level() -> int:
    """Keep prompt the user for a level until it gets a number between 1 and 3."""
    while True:
        try:
            level = int(input("Level: "))
        except ValueError:
            continue
        except EOFError:
            sys.exit("\nChallenge canceled!")

        if 1 <= level <= 3:
            return level


def generate_integer(digit_count) -> int:
    """Generate a number with {digit_count} digits."""
    try:
        digit_count = int(digit_count)
    except ValueError:
        raise ValueError("digit_count must be a number")

    if not (1 <= digit_count <= 3):
        raise ValueError("not (1 <= digit_count <= 3)")

    if digit_count != 1:
        return random.randint(10 ** (digit_count - 1), 10**digit_count - 1)
    else:
        return random.randint(0, 9)


def main():
    """Randomly generates ten (10) math problems."""
    level = get_level()
    score = 0

    for _ in range(MATH_PROBLEMS):
        num1 = generate_integer(level)
        num2 = generate_integer(level)

        for k in range(ATTEMPS):
            try:
                answer = int(input(f"{num1} + {num2} = "))
            except ValueError:
                print("EEE")
                continue
            except EOFError:
                sys.exit("\nChallenge canceled!")

            if answer == num1 + num2:
                score += 1
                break
            else:
                print("EEE")
        # If after 3 tries, stupid user still cannot solve
        else:
            print(f"{num1} + {num2} = {num1 + num2}")

    print(f"Score: {score}")


if __name__ == "__main__":
    main()
