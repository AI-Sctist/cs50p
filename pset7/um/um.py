import re
import sys


def count(s: str) -> int:
    return len(re.findall(r"(^| )um([,?\.]| |$)", s, re.IGNORECASE))


def main() -> None:
    print(count(input("Text: ")))


if __name__ == "__main__":
    main()
