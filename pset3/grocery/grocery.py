def main():
    grocery = dict()

    while True:
        try:
            name = input().upper()
        except EOFError:
            break

        count = grocery.get(name, 0)
        grocery.update({name: count + 1})

    grocery = sorted(grocery.items())

    for name, count in grocery:
        print(count, name)


if __name__ == "__main__":
    main()
