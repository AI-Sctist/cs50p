def main():
    # Prompt user for an arithmetic expression
    term1, operator, term2 = input("Expression: ").split()

    term1 = int(term1)
    term2 = int(term2)

    match operator:
        case "+":
            print(f"{term1+term2:.1f}")
        case "-":
            print(f"{term1-term2:.1f}")
        case "*":
            print(f"{term1*term2:.1f}")
        case _:
            print(f"{term1/term2:.1f}")


if __name__ == "__main__":
    main()
