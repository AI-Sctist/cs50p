def isvalid(plate):
    if len(plate) < 2 or len(plate) > 6:
        return False

    if not plate[0:2].isalpha():
        return False

    for i in range(len(plate)):
        # Case: the leading digit is zero or not
        if plate[i].isdecimal():
            if plate[i] == '0' and (i == 0 or plate[i-1].isalpha()):
                return False

        # Case: numbers are used in the middle or not
        elif plate[i].isalpha():
            if i > 0 and plate[i-1].isdecimal():
                return False

        # Case: plate contains characters not allowed
        else:
            return False

    return True


def main():
    plate = input("Plate: ")

    if isvalid(plate):
        print("Valid")
    else:
        print("Invalid")


if __name__ == "__main__":
    main()
