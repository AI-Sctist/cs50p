import re
import sys


def convert(s: str) -> str:
    match = re.fullmatch(
        r"(\d\d?(?::\d\d?)? [A|P]M) to (\d\d?(?::\d\d?)? [A|P]M)",
        s,
    )
    if match:
        start = format_24hour(match.group(1))
        end = format_24hour(match.group(2))
        if start[0] == 12 and end[0] == 0:
            start, end = end, start
        return f"{start[0]:02d}:{start[1]:02d} to {end[0]:02d}:{end[1]:02d}"
    else:
        raise ValueError("Incorrect time format")


def format_24hour(input_time: str) -> tuple[int, int]:
    time, meridiem = input_time.split(" ")
    try:
        hour, minute = time.split(":")
        hour, minute = int(hour), int(minute)
    except ValueError:
        hour, minute = int(time), int(0)

    if not (0 < hour <= 12 and 0 <= minute < 60):
        raise ValueError("Invalid time")

    hour = (hour + 12 * (meridiem == "PM")) % 24
    return (hour, minute)


def main() -> None:
    print(convert(input("Hours: ").strip()))


if __name__ == "__main__":
    main()
