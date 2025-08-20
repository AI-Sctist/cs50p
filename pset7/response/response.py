import validators


def main() -> None:
    if validators.email(input("What's your email address? ")):
        print("Valid")
    else:
        print("Invalid")


if __name__ == "__main__":
    main()
