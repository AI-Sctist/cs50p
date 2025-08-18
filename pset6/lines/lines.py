from sys import argv
from sys import exit


def line_count(file_name):
    """Count the number of lines of code, excluding blank lines and comments."""
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        exit("File does not exist")

    count = 0

    for line in file:
        code = line.strip()
        if not (len(code) == 0 or code[0] == "#"):
            count += 1

    file.close()
    return count


def main():
    """Grade the complexity of code base on its number of lines."""
    if len(argv) < 2:
        exit("Too few command-line arguments")
    elif len(argv) > 2:
        exit("Too many command-line arguments")

    file_name = argv[1]

    if file_name[-3:] != ".py":
        exit("Not a python file")

    print(line_count(file_name))


if __name__ == "__main__":
    main()
