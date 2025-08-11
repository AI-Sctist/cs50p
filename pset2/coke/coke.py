def main():
    print("Amount Due: 50")
    amount_due = 50

    while True:
        coin = int(input("Insert coin: "))

        if coin in [25, 10, 5]:
            amount_due -= coin

        if amount_due <= 0:
            print("Change Owed:", abs(amount_due))
            break
        else:
            print("Amount Due:", amount_due)


if __name__ == "__main__":
    main()
