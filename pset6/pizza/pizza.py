import csv
import sys
from tabulate import tabulate


def read_content(file_name):
    try:
        csv_file = open(file_name, "r", newline="")
    except FileNotFoundError:
        sys.exit("File does not exist")

    table_data = []

    for row in csv.reader(csv_file):
        table_data.append(row)

    return table_data

def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    if len(sys.argv[1]) < 4 or sys.argv[1][-4:] != ".csv":
        sys.exit("Not a csv file")

    content = read_content(sys.argv[1])

    print(tabulate(content, headers="firstrow", tablefmt="grid"))


if __name__ == "__main__":
    main()
