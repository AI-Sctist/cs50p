import re
import sys

GIFT_FOR_CODE_READERS = r"https://youtu.be/xvFZjo5PgG0"  # :))


def parse(s: str) -> str | None:
    # Expect a valid youtube embed html code
    # Return a shorter and sharable link
    match = re.fullmatch(
        r'<iframe[^>]*src="(https?://(?:www\.)?youtube\.com/embed/[^"]*)"[^>]*></iframe>',
        s,
    )
    if match:
        url = match.group(1)
        url = url.replace("www.", "").replace("youtube.com/embed", "youtu.be")
        url = url.replace("http://", "https://")
        return url
    else:
        return None


def main() -> None:
    print(parse(input("HTML: ")))


if __name__ == "__main__":
    main()
