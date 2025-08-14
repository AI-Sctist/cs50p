import inflect

# Contains a formatter (join() for grouping words into an Oxford-comma string)
ENGINE = inflect.engine()


def main():
    """Say adieu to users using Oxford comma to seperate."""
    people = []

    while True:
        try:
            name = input("Name: ")
        except EOFError:
            print("\n", end="")
            break

        people.append(name)

    # Say "adieu" to people
    print(f"Adieu, adieu, to {ENGINE.join(people)}")


if __name__ == "__main__":
    main()
