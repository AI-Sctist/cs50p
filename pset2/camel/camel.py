def snakecase(camel_case):
    """Convert from camelCase to snake_case."""
    words = []

    cur1 = 0
    for cur2 in range(len(camel_case)):
        if camel_case[cur2].isupper():
            words.append(camel_case[cur1:cur2].lower())
            cur1 = cur2

    # Add the missing word at the end
    words.append(camel_case[cur1:].lower())

    return "_".join(words)


def main():
    camel_case = input("camelCase: ")
    print("snake_case: " + snakecase(camel_case))


if __name__ == "__main__":
    main()
