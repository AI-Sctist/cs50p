def main():
    menu = {
        "baja taco": 4.25,
        "burrito": 7.50,
        "bowl": 8.50,
        "nachos": 11.00,
        "quesadilla": 8.50,
        "super burrito": 8.50,
        "super quesadilla": 9.50,
        "taco": 3.00,
        "tortilla salad": 8.00,
    }

    total_price = 0

    while True:
        try:
            food = input("Item: ")
        except EOFError:
            print("\n", end="")
            break

        price = menu.get(food.lower(), "Not_found")

        if price != "Not_found":
            total_price += price
            print(f"Total: ${total_price:.2f}")


if __name__ == "__main__":
    main()
