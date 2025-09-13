import datetime
import os
import sys

from rich import print
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()  # Module attribute :))


class TransactionParser:
    def __init__(self, controller, subcommand, arguments):
        self.controller = controller
        self.subcommand = subcommand
        self.arguments = normalize(arguments)

        if subcommand == "list":
            self.list_transaction()
        elif subcommand == "add":
            self.add_transaction()
        elif subcommand == "update":
            self.update_transaction()
        elif subcommand == "delete":
            self.delete_transaction()
        elif subcommand == "filter":
            self.filter_transaction()
        else:
            raise Exception("Unsupported subcommand")

    def list_transaction(self):
        remain = int(self.arguments[0])
        if remain <= 0:
            raise ValueError("Number of transactions to show must be positive")

        # Set up table
        transaction_table = Table(title="Transaction History")
        transaction_table.add_column("ID", style="cyan", no_wrap=True)
        transaction_table.add_column("Type", style="magenta")
        transaction_table.add_column("Category", style="green")
        transaction_table.add_column("Amount", justify="right", style="red")
        transaction_table.add_column("Date Time", style="yellow")
        transaction_table.add_column("Note", style="white")

        # Show data
        with Live(transaction_table, console=console, refresh_per_second=4) as live:
            for transaction in self.controller.get_all_transactions():
                transaction_table.add_row(
                    transaction["id"],
                    transaction["type"],
                    transaction["category"],
                    transaction["amount"],
                    transaction["date_time"],
                    transaction["note"] if transaction["note"] else "-",
                )
                live.update(transaction_table)

                remain -= 1
                if remain == 0:
                    break

    def add_transaction(self):
        # Get user input
        type, amount, category, date_time, note = self.get_transaction_fields()

        # Save transaction
        self.controller.save_transaction(
            type=type, amount=amount, category=category, date_time=date_time, note=note
        )
        print("Transaction added successfully.")

    def update_transaction(self):
        # Get user input
        type, amount, category, date_time, note = self.get_transaction_fields()
        id = self.arguments[0]

        # Prepare kwargs for update
        kwargs = {}
        if type is not None:
            kwargs.update({"type": type})
        if amount is not None:
            kwargs.update({"amount": amount})
        if category is not None:
            kwargs.update({"category": category})
        if date_time is not None:
            kwargs.update({"date_time": date_time})
        if note != "":
            kwargs.update({"note": note})

        # Update transaction
        self.controller.update_transaction(id, **kwargs)
        print("Transaction updated successfully.")

    def delete_transaction(self):
        id = self.arguments[0]
        self.controller.delete_transaction(id)
        print("Transaction deleted successfully.")

    def filter_transaction(self):
        fieldname = self.arguments[0].lstrip("-")
        args = self.arguments[1:]
        self.controller.filter_by(fieldname, *args)

    def get_transaction_fields(self):
        """
        These are default values of transaction fields. If type, amount, category are not
        provided, the program will pass None to controller, leading to validation error
        """

        # Default values
        type = None
        amount = None
        category = None
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = ""

        # Optional values
        for arg in self.arguments:
            match arg:
                case "-t":
                    type = self.arguments[self.arguments.index(arg) + 1]
                case "-a":
                    amount = self.arguments[self.arguments.index(arg) + 1]
                case "-c":
                    category = self.arguments[self.arguments.index(arg) + 1]
                case "-d":
                    date_time = self.arguments[self.arguments.index(arg) + 1]
                case "-n":
                    note = self.arguments[self.arguments.index(arg) + 1]

        return type, amount, category, date_time, note


class CategoryParser:
    def __init__(self, controller, subcommand, arguments):
        self.controller = controller
        self.subcommand = subcommand
        self.arguments = normalize(arguments)

        if subcommand == "list":
            self.list_category()
        elif subcommand == "add":
            self.add_category()
        elif subcommand == "remove":
            self.remove_category()
        else:
            raise Exception("Unsupported subcommand")

    def list_category(self):
        for category in self.controller.get_categories():
            print(f"- {category}")

    def add_category(self):
        category = self.arguments[0]
        self.controller.add_category(category)
        print(f"Category '{category}' added successfully.")

    def remove_category(self):
        category = self.arguments[0]
        self.controller.remove_category(category)
        print(f"Category '{category}' removed successfully.")


class statisticsParser:
    def __init__(self, controller, subcommand):
        self.controller = controller
        self.subcommand = subcommand

        # Currently only support expense by category
        if subcommand == "expense":
            self.expense_by_category()
        elif subcommand == "income":
            # Not promised feature :)) give me money first
            print("Support income by category later")
        else:
            raise Exception("Unsupported subcommand")

    def expense_by_category(self):
        stats, total = self.controller.stats_expense_by_category()

        # Set up table
        stats_table = Table(title="Expense by Category")
        stats_table.add_column("Category", style="cyan")
        stats_table.add_column("Amount", justify="right", style="red")
        stats_table.add_column("Percentage", justify="right", style="green")

        # Show data
        for category, amount in stats.items():
            percentage = (amount / total * 100) if total > 0 else 0
            stats_table.add_row(category, str(amount), f"{percentage:.2f}%")

        Console().print(stats_table)


def show_welcome():
    print("\n=============================================")
    print("   Finance CLI  v0.1")
    print("   Personal Finance Manager for Developers")
    print("=============================================\n")
    print("Type 'help'   to see all commands")
    print("Type 'exit'   to quit\n")


def show_help():
    print(
        """
📘 Available Commands
=====================

🔹 transaction (tx) <subcommand> [options]  → Manage transactions
    Subcommands:")
      • list <number>")
          List recent transactions")
      • add -t <type> -a <amount> -c <category> [-d <date>] [-n <note>]
          Add a new transaction")
      • update <id> [-t <type>] [-a <amount>] [-c <category>] [-d <date>] [-n <note>]
          Update an existing transaction
      • delete <id>
          Delete a transaction
      • filter --<fieldname> <value(s)>
          Filter transactions by field (type, category, date_time, amount, note)

🔹 category (cat) <subcommand> [options]   → Manage categories
    Subcommands:
      • list
          List all categories
      • add <category>
          Add a new category
      • remove <category>
          Remove a category

🔹 balance (bal)                           → Show current income, expense, and balance

🔹 statistics (stats) <subcommand>         → Show financial statistics
    Subcommands:
      • expense
          Show expense breakdown by category

🔹 help                                    → Show this help message
🔹 clear                                   → Clear the console screen
🔹 exit | quit                             → Exit the application
          """
    )


def show_goodbye():
    print("\n==============================================")
    print("Thanks for using Finance CLI")
    print("Code hard 💻 • Spend smart 💰 • Save more 📈")
    print("==============================================\n")


def show_finance(controller):
    income = controller.get_income()
    expense = controller.get_expense()
    balance = controller.get_balance()
    print(f"Income:  {income}")
    print(f"Expense: {expense}")
    print(f"Balance: {balance}")


def normalize(a_list):
    return [element.lower().strip() for element in a_list]


def run_application(controller):
    """
    Exception handling strategy:
    - If missing args, the program auto raise IndexError
    - If invalid args, the program auto raise ValueError
    - All exceptions are caught by interpreter :))
    """

    show_welcome()
    while True:
        user_command = input("fincli> ").strip().lower()
        parts = user_command.split(" ")
        command = parts[0]
        subcommand = parts[1] if len(parts) > 1 else ""
        arguments = parts[2:] if len(parts) > 2 else []

        if command in ["transaction", "tx"]:
            try:
                TransactionParser(controller, subcommand, arguments)
            except Exception as e:
                print(f"Error {e}")

        elif command in ["category", "cat"]:
            try:
                CategoryParser(controller, subcommand, arguments)
            except Exception as e:
                print(f"Error {e}")

        elif command in ["balance", "bal"]:
            show_finance(controller)

        elif command in ["statistics", "stats"]:
            try:
                statisticsParser(controller, subcommand)
            except Exception as e:
                print(f"Error {e}")

        elif command == "help":
            show_help()

        elif command == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        elif command == "exit" or command == "quit":
            show_goodbye()
            sys.exit(0)

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' to see all commands")
