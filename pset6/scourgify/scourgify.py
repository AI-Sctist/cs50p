import csv
import sys


def check_csv_extension(file_name):
    if len(file_name) < 4 or file_name[-4:] != ".csv":
        sys.exit(f"{file_name} is not a csv file")


def read_content(file_name):
    content = []

    try:
        with open(file_name, "r", newline="") as file:
            data = csv.reader(file)
            next(data)
            for row in data:
                content.append(row)
    except FileNotFoundError:
        sys.exit(f"Could not read {file_name}")

    return content


def formatted(content):
    for row in content:
        last_name, first_name = row[0].split(", ")
        row[0:1] = [first_name, last_name]


def write_content(file_name, content):
    header = ["first", "last", "house"]

    try:
        with open(file_name, "w", newline="") as file:
            pen = csv.writer(file)
            pen.writerow(header)
            for row in content:
                pen.writerow(row)
    except FileNotFoundError:
        sys.exit(f"Could not read {file_name}")


def main():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    check_csv_extension(sys.argv[1])
    check_csv_extension(sys.argv[2])

    content = read_content(sys.argv[1])

    # Pass by reference
    formatted(content)

    write_content(sys.argv[2], content)


if __name__ == "__main__":
    main()
