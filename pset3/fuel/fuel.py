def main():
    while True:
        fraction = input("Fraction: ")
        split_pos = fraction.find("/")

        # Case: num1, num2 are not intergers
        try:
            num1 = int(fraction[:split_pos])
            split_pos += 1
            num2 = int(fraction[split_pos:])
        except ValueError:
            continue

        # Case: num2 is zero
        try:
            percent = round(num1 / num2 * 100)
        except ZeroDivisionError:
            continue

        # Case: percent is greater than 100 or negative
        if percent > 100 or percent < 0:
            continue

        if percent >= 99:
            print("F")
        elif percent <= 1:
            print("E")
        else:
            print(f"{percent}%")

        # Pass all exceptions -> break :)
        break


if __name__ == "__main__":
    main()
