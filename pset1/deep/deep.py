def main():
    answer = input(
        "What is the Answer to the Great Question of Life, the Universe, and Everything? "
    ).lower()

    if (
        answer.find("42") != -1
        or answer.find("forty-two") != -1
        or answer.find("forty two") != -1
    ):
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()
