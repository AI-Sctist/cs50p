import csv
import datetime
import os
import sys

from rich import print
from rich.console import Console
from rich.live import Live
from rich.table import Table


# ==============================
#          UTILITIES           |
# ==============================


def normalize(a_list):
    return [element.lower().strip() for element in a_list]


def percentage(amount, total, decimals=2):
    per = (amount / total * 100) if total > 0 else 0
    return f"{per:.{decimals}f}"


def initialize_database():
    def write_header():
        with open(transactions, "w", newline="") as file:
            csv.DictWriter(
                file,
                fieldnames=repositories.TransactionRepository.FIELDNAMES,
            ).writeheader()

    # Project root
    root = os.path.dirname(os.path.abspath(__file__))

    # Database does not exist
    database = os.path.join(root, "database")
    if not os.path.exists(database):
        os.mkdir("database")

    # Place for temporary files does not exist
    temporary_files = os.path.join(database, "temporary_files")
    tmp_txt = os.path.join(temporary_files, "tmp.txt")
    tmp_csv = os.path.join(temporary_files, "tmp.csv")
    if not os.path.exists(temporary_files):
        os.mkdir(temporary_files)
        with open(tmp_txt, "w"), open(tmp_csv, "w"):
            pass

    # Transaction fields are incorrect
    transactions = os.path.join(database, "transactions.csv")
    if not os.path.exists(transactions):
        write_header()
    else:
        with open(transactions, "r", newline="") as inp:
            if (
                csv.DictReader(inp).fieldnames
                != repositories.TransactionRepository.FIELDNAMES
            ):
                write_header()

    # Initialize default categories
    categories = os.path.join(database, "categories.txt")
    if not os.path.exists(categories) or os.path.getsize(categories) == 0:
        with open(categories, "w") as file:
            for cat in repositories.CategoryRepository.DEFAULT:
                file.write(cat + "\n")

    # Return path (for reusability)
    return {
        "root": root,
        "database": database,
        "transactions": transactions,
        "categories": categories,
        "temporary_files": temporary_files,
        "tmp_csv": tmp_csv,
        "tmp_txt": tmp_txt,
    }


# ==============================
#         PRESENTATION         |
# ==============================


class ui_components:
    """
    UI components module
    """

    console = Console()

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
            with Live(
                transaction_table, console=ui_components.console, refresh_per_second=4
            ) as live:
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
                type=type,
                amount=amount,
                category=category,
                date_time=date_time,
                note=note,
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
            These are default values of transaction fields. If type, amount, category are
            not provided, the program will pass None to controller, leading to validation
            error.
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
                stats_table.add_row(
                    category, str(amount), str(percentage(amount, total)) + "%"
                )

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

    def run_application(controller):
        """
        Exception handling strategy:
        - If missing args, the program auto raise IndexError
        - If invalid args, the program auto raise ValueError
        - All exceptions are caught by interpreter :))
        """

        ui_components.show_welcome()
        while True:
            user_command = input("fincli> ").strip().lower()
            parts = user_command.split(" ")
            command = parts[0]
            subcommand = parts[1] if len(parts) > 1 else ""
            arguments = parts[2:] if len(parts) > 2 else []

            if command in ["transaction", "tx"]:
                try:
                    ui_components.TransactionParser(controller, subcommand, arguments)
                except Exception as e:
                    print(f"Error {e}")

            elif command in ["category", "cat"]:
                try:
                    ui_components.CategoryParser(controller, subcommand, arguments)
                except Exception as e:
                    print(f"Error {e}")

            elif command in ["balance", "bal"]:
                ui_components.show_finance(controller)

            elif command in ["statistics", "stats"]:
                try:
                    ui_components.statisticsParser(controller, subcommand)
                except Exception as e:
                    print(f"Error {e}")

            elif command == "help":
                ui_components.show_help()

            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif command == "exit" or command == "quit":
                ui_components.show_goodbye()
                sys.exit(0)

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' to see all commands")


class controller:
    """
    Controller module
    """

    class Controller:
        def __init__(
            self,
            transaction_manager,
            category_manager,
            category,
            user,
            transaction_validation,
            user_service,
            transaction_service,
        ):
            # Data access
            self.transaction_manager = transaction_manager
            self.category_manager = category_manager

            # Entities
            self.category = category
            self.user = user

            # Validation
            self.transaction_validation = transaction_validation

            # Services
            self.user_service = user_service
            self.transaction_service = transaction_service

        def get_income(self):
            return self.user.income

        def get_expense(self):
            return self.user.expense

        def get_balance(self):
            return self.user.balance

        def save_transaction(self, **kwargs):
            self.transaction_validate(**kwargs)
            self.transaction_service.create(self.user, **kwargs)
            self.user_service.apply_transaction(kwargs["type"], int(kwargs["amount"]))

        def update_transaction(self, id, **kwargs):
            self.transaction_validate(**kwargs)
            if (
                transaction_info := self.transaction_service.update(id, **kwargs)
            ) is not None:
                self.user_service.apply_transaction(
                    transaction_info["type_old"],
                    int(transaction_info["amount_old"]),
                    transaction_info["type_new"],
                    int(transaction_info["amount_new"]),
                )

        def delete_transaction(self, id):
            if (transaction_info := self.transaction_service.delete(id)) is not None:
                self.user_service.revert_transaction(
                    transaction_info["type"], int(transaction_info["amount"])
                )

        def get_all_transactions(self):
            return self.transaction_service.readall()

        def transaction_validate(self, **kwargs):
            """
            Remember: all data are in string format when received from UI
            """

            for field, value in kwargs.items():
                match field:
                    case "type":
                        if not self.transaction_validation.type_validate(value):
                            raise ValueError(f"Invalid type: {value}")
                    case "amount":
                        if not self.transaction_validation.amount_validate(value):
                            raise ValueError(f"Invalid amount: {value}")
                    case "category":
                        if not self.transaction_validation.category_validate(value):
                            raise ValueError(f"Invalid category: {value}")
                    case "date_time":
                        if not self.transaction_validation.date_time_validate(value):
                            raise ValueError(f"Invalid date and time: {value}")
                    case "note":
                        # Note can be any string, no validation needed
                        pass
                    case _:
                        raise ValueError(f"Unknown field: {field}")

        def filter_by(self, fieldname, *args):
            """
            args usage depends on fieldname:
            "category": <category>
            "type": <type>
            "date_time": <start_date>, <end_date>
            "amount": <min_amount>, <max_amount>
            """

            match fieldname:
                case "category":
                    return self.transaction_service.filter_by_category(*args)
                case "type":
                    return self.transaction_service.filter_by_type(*args)
                case "date_time":
                    return self.transaction_service.filter_by_date_range(*args)
                case "amount":
                    return self.transaction_service.filter_by_amount_range(*args)
                case _:
                    raise ValueError(f"Not support fieldname: {fieldname}")

        def stats_expense_by_category(self):
            """
            Return dict(category: <total_expense>) and total(for percentage calculation)
            """

            stats = {}
            total = 0
            for category in self.category.categories:
                stats[category] = 0

            for transaction in self.transaction_service.filter_by_type("expense"):
                total += int(transaction["amount"])
                stats[transaction["category"]] += int(transaction["amount"])

            return stats, total

        # Income by category not promised feature :))
        # Give me money first (-_-)

        def get_categories(self):
            return list(self.category.categories)

        def add_category(self, category):
            # Database
            if category not in self.category.categories:
                self.category_manager.create(category)

            # State
            self.category.create(category)

        def remove_category(self, category):
            # Database
            self.category_manager.delete(category)

            # State
            self.category.delete(category)


# ==============================
#        BUSINESS LOGIC        |
# ==============================


class entities:
    """
    Entities module
    """

    class Transaction:
        """
        Contains the attributes of a transaction. Can only be changed via the service module
        for data validation

        Requirements:
            - do not contain white spaces at both ends
            - type and category are in lowercase
        """

        def __init__(self, id, type, amount, date_time, category, note):
            self._id = id
            self._type = type
            self._amount = int(amount)
            self._date_time = date_time
            self._category = category
            self._note = note

        @property
        def id(self):
            return self._id

        @property
        def type(self):
            return self._type

        @property
        def amount(self):
            return self._amount

        @property
        def date_time(self):
            return self._date_time

        @property
        def category(self):
            return self._category

        @property
        def note(self):
            return self._note

        def _set_type(self, value):
            self._type = value

        def _set_amount(self, value):
            self._amount = value

        def _set_date_time(self, value):
            self._date_time = value

        def _set_category(self, value):
            self._category = value

        def _set_note(self, value):
            self._note = value

    class Categories:
        """
        Contains the pre-defined and user-defined categories

        Requirements:
            - do not contain white spaces at both ends
            - all cats are in lowercase
        """

        def __init__(self, categories):
            self._categories = set(categories)

        @property
        def categories(self):
            return self._categories

        def create(self, category):
            self._categories.add(category)

        def delete(self, category):
            self._categories.discard(category)

    class User:
        """
        Contains the user's income and expense. Can only be changed via the service module
        """

        def __init__(self, transaction_history):
            self._transaction_count = 0
            self._income = 0
            self._expense = 0

            for transaction in transaction_history:
                self._transaction_count += 1
                if transaction["type"] == "income":
                    self._income += int(transaction["amount"])
                else:
                    self._expense += int(transaction["amount"])

        @property
        def transaction_count(self):
            return self._transaction_count

        @property
        def income(self):
            return self._income

        @property
        def expense(self):
            return self._expense

        @property
        def balance(self):
            return self.income - self.expense


class services:
    """
    Services module
    """

    class UserService:
        """
        Change user's income and expense according to the info of the transaction created or
        deleted by user
        """

        def __init__(self, user):
            self.user = user

        def apply_transaction(self, type_old, amount_old, type_new, amount_new):
            if type_old == "income":
                self.user._income -= amount_old
            elif type_old == "expense":
                self.user._expense -= amount_old
            else:
                raise ValueError(f"Unknown transaction type: {type_old}")

            if type_new == "income":
                self.user._income += amount_new
            elif type_new == "expense":
                self.user._expense += amount_new
            else:
                raise ValueError(f"Unknown transaction type: {type_new}")

        def revert_transaction(self, type, amount):
            if type == "income":
                self.user._income -= amount
            elif type == "expense":
                self.user._expense -= amount
            else:
                raise ValueError(f"Unknown transaction type: {type}")

    class TransactionService:
        def __init__(self, transaction_repository):
            self.id_digit_amount = 9
            self.data_access = transaction_repository

        def create(self, user, **kwargs):
            # Generate transaction id using auto-increment (transaction count)
            transaction = entities.Transaction(
                f"{user.transaction_amount:0{self.id_digit_amount}d}", **kwargs
            )

            self.data_access.create(transaction.__dict__)

        def readall(self):
            return self.data_access.readall()

        def update(self, id, **kwargs):
            # Transaction id cannot be updated, only generated once when created
            if "id" in kwargs:
                raise ValueError("Transaction id cannot be updated")

            return self.data_access.update(id, kwargs)

        def delete(self, id):
            """
            Delete a specified transaction and return a dict(type, amount) for UserService
            """
            return self.data_access.delete(id)

        def filter_by_category(self, category):
            for transaction in self.data_access.readall():
                if transaction["category"] == category:
                    yield transaction

        def filter_by_date_range(self, start_date, end_date):
            """
            Format of date_time: YYYY-MM-DD HH:MM:SS
            """
            for transaction in self.data_access.readall():
                if start_date <= transaction["date_time"] <= end_date:
                    yield transaction

        def filter_by_type(self, type):
            for transaction in self.data_access.readall():
                if transaction["type"] == type:
                    yield transaction

        def filter_by_amount_range(self, min_amount, max_amount):
            for transaction in self.data_access.readall():
                if int(min_amount) <= int(transaction["amount"]) <= int(max_amount):
                    yield transaction

        # Add sort by transaction fields
        ...

    # class CategoryService: is in entities (Categories)


class validation:
    """
    Validation module
    """

    class TransactionValidation:
        """
        Validate transaction fields from controller before passing to services
        """

        def __init__(self, categories):
            self.defined_categories = set(categories)  # Store state, so use class

        def type_validate(self, value):
            return value in ["income", "expense"]

        def amount_validate(self, value):
            try:
                return int(value) > 0
            except ValueError:
                return False

        def date_time_validate(self, value):
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False

        def category_validate(self, value):
            return value in self.defined_categories


# ==============================
#         DATA ACCESS          |
# ==============================


class repositories:
    """
    Repositories module
    """

    class TransactionRepository:
        FIELDNAMES = ["id", "type", "amount", "date_time", "category", "note"]

        def __init__(self):
            # Get database root path
            root = os.path.dirname(os.path.abspath(__file__))
            database = os.path.join(root, "database")

            # Transaction history
            self.file_path = os.path.join(database, "transactions.csv")

            # Temporary files
            self.tmp = os.path.join(database, "temporary_files", "tmp.csv")

        def create(self, transaction):
            with open(self.file_path, "a", newline="") as file:
                pen = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                pen.writerow(transaction)

        def readall(self):
            with open(self.file_path, "r", newline="") as file:
                for transaction in csv.DictReader(file):
                    yield transaction

        def update(self, id, **kwargs):
            """
            Return a dict(type_old, amount_old, type_new: amount_new) of the transaction
            for calculating user's balance
            """

            # Helper function for changing data fields
            def change(transaction):
                for key, value in kwargs.items():
                    transaction[key] = value

            # Return data
            return_data = None

            # Temporary store data
            with (
                open(self.file_path, "r", newline="") as src,
                open(self.tmp, "w", newline="") as dst,
            ):
                pen = csv.DictWriter(dst, fieldnames=self.FIELDNAMES)
                pen.writeheader()
                for transaction in csv.DictReader(src):
                    if transaction["id"] == id:
                        return_data = {
                            "type_old": transaction["type"],
                            "amount_old": transaction["amount"],
                            "type_new": kwargs.get("type", transaction["type"]),
                            "amount_new": kwargs.get("amount", transaction["amount"]),
                        }
                        change(transaction)
                    pen.writerow(transaction)

            # Write to src file
            os.replace(self.tmp, self.file_path)

            return return_data

        def delete(self, id):
            """
            Delete a transaction in the database, return a dict(type, amount) of the
            transaction for calculating user's balance
            """

            # Return data
            return_data = None

            # Temporary store data
            with (
                open(self.file_path, "r", newline="") as src,
                open(self.tmp, "w", newline="") as dst,
            ):
                pen = csv.DictWriter(dst, fieldnames=self.FIELDNAMES)
                pen.writeheader()
                for transaction in csv.DictReader(src):
                    if transaction["id"] != id:
                        pen.writerow(transaction)
                    else:
                        return_data = {
                            "type": transaction["type"],
                            "amount": transaction["amount"],
                        }

            # Write to src file
            os.replace(self.tmp, self.file_path)

            return return_data

    class CategoryRepository:
        DEFAULT = [
            "food",
            "transportation",
            "contact fee",
            "clothes",
            "electric bill",
            "medical",
            "housing expense",
            "exchange",
            "houseware",
            "cosmetic",
            "education",
        ]

        def __init__(self):
            # Get database root path
            root = os.path.dirname(os.path.abspath(__file__))
            database = os.path.join(root, "database")

            # Defined categories
            self.file_path = os.path.join(database, "categories.txt")

            # Temporary files
            self.tmp = os.path.join(database, "temporary_files", "tmp.txt")

        def create(self, category):
            with open(self.file_path, "a") as file:
                file.write(category + "\n")

        def readall(self):
            with open(self.file_path, "r") as file:
                for category in file:
                    yield category.strip()

        def delete(self, name):
            # Temporary store data
            with open(self.file_path, "r") as src, open(self.tmp, "w") as dst:
                for category in src:
                    category = category.strip()
                    if category != name:
                        dst.write(category + "\n")

            # Change name and directory of the tmp file to the main file, then delete
            # the main file
            os.replace(self.tmp, self.file_path)


def main():
    # Check for the existence of the database, if not, initialize it
    initialize_database()

    # Repositories
    transaction_repo = repositories.TransactionRepository()
    category_repo = repositories.CategoryRepository()

    # Entities
    user = entities.User(transaction_repo.readall())
    categories = entities.Categories(category_repo.readall())

    # Validation
    transaction_validation = validation.TransactionValidation(category_repo.readall())

    # Services
    user_service = services.UserService(user)
    transaction_service = services.TransactionService(transaction_repo)

    # Controller
    backend_controller = controller.Controller(
        transaction_repo,
        category_repo,
        categories,
        user,
        transaction_validation,
        user_service,
        transaction_service,
    )

    # Run
    app = ui_components
    app.run_application(backend_controller)


if __name__ == "__main__":
    main()
