def shorten(sentence):
    """Remove all vowels in a sentence."""
    shorter = []

    for char in sentence:
        if char.lower() not in ['a', 'e', 'i', 'o', 'u']:
            shorter.append(char)

    return "".join(shorter)


def main():
    sentence = input("Input: ")
    print("Output:", shorten(sentence))


if __name__ == "__main__":
    main()
