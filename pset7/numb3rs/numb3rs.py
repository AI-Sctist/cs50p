import re
import sys


def validate(ip) -> bool:
    condition = r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)"
    return (
        re.fullmatch(
            rf"{condition}\.{condition}\.{condition}\.{condition}",
            ip,
        )
        is not None
    )


def main() -> None:
    print(validate(input("IPv4 Address: ")))


if __name__ == "__main__":
    main()
