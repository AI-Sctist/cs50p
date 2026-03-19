def convert_to_iso(date):
    """Convert from format month/day/year to ISO 8601"""

    def format_to_iso(parts):
        try:
            month = int(parts[0])
            day = int(parts[1])
            year = int(parts[2])
        except ValueError:
            return False
        else:
            return (
                False
                if not (1 <= month <= 12 and 1 <= day <= 31 and year > 0)
                else f"{year:04d}-{month:02d}-{day:02d}"
            )

    # Use to convert a month from word to number
    in_number = {
        "january": "1",
        "february": "2",
        "march": "3",
        "april": "4",
        "may": "5",
        "june": "6",
        "july": "7",
        "august": "8",
        "september": "9",
        "october": "10",
        "november": "11",
        "december": "12",
    }

    # Try a format like 6/27/2008
    parts = date.split("/")
    if len(parts) == 3:
        iso_date = format_to_iso(parts)
        if iso_date != False:
            return iso_date

    # Try a format like June 27, 2008
    parts = date.split(" ")
    if len(parts) == 3 and parts[1][-1] == ",":
        # Remove "," after the day
        parts[1] = parts[1][:-1]
        parts[0] = in_number.get(parts[0].lower(), "0")

        iso_date = format_to_iso(parts)
        if iso_date != False:
            return iso_date

    return False


def main():
    while True:
        date = input("Date: ")
        iso_date = convert_to_iso(date.strip())

        if iso_date != False:
            break

    print(iso_date)


if __name__ == "__main__":
    main()
