import csv
import datetime
import os
import sys

from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.prompt import Prompt

CONSOLE = Console()

DATAFILE = "transactions.csv"
HEADER = ["Date", "Amount", "Type", "Category", "Description"]
AVAILABLE_CATEGORIES = [
    "food", "transportation", "clothes", "medical",
    "electric bill", "housing expense", "houseware",
    "contact fee", "exchange", "cosmetic", "education", "other",
]


class Transaction:
    def __init__(self, date, amount, type, category, description):
        self.date = date
        self.amount = amount
        self.type = type
        self.category = category
        self.description = description

    def _type_validate(self):
        return self.type in ["income", "expense"]

    def _amount_validate(self):
        try:
            return int(self.amount) > 0
        except ValueError:
            return False

    def _date_time_validate(self):
        try:
            if len(self.date) == 10:
                datetime.datetime.strptime(self.date, "%Y-%m-%d")
            else:
                datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    def _category_validate(self):
        return self.category in AVAILABLE_CATEGORIES

    def validate(self):
        return self._type_validate() and self._amount_validate() and \
            self._date_time_validate() and self._category_validate()


class User:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self._load_data()

    def _load_data(self):
        with open(DATAFILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                date, amount, type, category, description = row
                if type == "income":
                    self.income += int(amount)
                else:
                    self.expenses += int(amount)


class NewTransactionHistory:
    def __init__(self, user):
        self.transactions = []
        self.user = user  # To update user balance in real time after each transaction modification

    def add_transaction(self):
        CONSOLE.print(Panel("[bold cyan]Add New Transaction[/bold cyan]", expand=False))
        date = Prompt.ask("Enter date (YYYY-MM-DD)", default=datetime.datetime.now().strftime("%Y-%m-%d"))
        amount = Prompt.ask("Enter amount", default="0")
        type = Prompt.ask("Enter type", choices=["income", "expense"], default="expense")
        category = Prompt.ask("Enter category", choices=AVAILABLE_CATEGORIES, default="other")
        description = Prompt.ask("Enter description")

        transaction = Transaction(date, amount, type, category, description)
        if transaction.validate():
            update_user_balance(self.user, amount, type, 1)
            self.transactions.append(transaction)
            CONSOLE.print("[bold green]✔ Transaction added successfully![/bold green]\n")
        else:
            CONSOLE.print("[bold red]✘ Invalid input, please try again![/bold red]\n")

    # Only for listing transactions
    def _display_table(self, title, data_list, is_old=False):
        table = Table(title=title, show_header=True, header_style="bold magenta", border_style="dim")
        table.add_column("ID", justify="center", style="dim")
        table.add_column("Date", style="cyan")
        table.add_column("Type")
        table.add_column("Category", style="yellow")
        table.add_column("Amount", justify="right")
        table.add_column("Description", style="italic")

        for i, t in enumerate(data_list, 1):
            color = "green" if t[2] == "income" else "red"
            table.add_row(str(i), t[0], f"[{color}]{t[2]}[/{color}]", t[3], f"{int(t[1]):,}", t[4])

        CONSOLE.print(table)

    def list_transactions(self):
        if self.transactions:
            data = [[t.date, t.amount, t.type, t.category, t.description] for t in self.transactions]
            self._display_table("Pending Transactions (Not Saved)", data)
        else:
            CONSOLE.print("[yellow]No new transactions pending[/yellow]")

        if Prompt.ask("View saved transaction history?", choices=["y", "n"], default="n") == "y":
            chunk = []
            count = 0
            with open(DATAFILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    chunk.append(row)
                    count += 1
                    if count % 10 == 0:
                        self._display_table(f"Saved Transactions (Page {count//10})", chunk)
                        chunk = []
                        if Prompt.ask("Show more?", choices=["y", "n"], default="y") == "n":
                            break

            # No old transactions at all
            if count == 0:
                CONSOLE.print("[red]No history found[/red]")
            # Handle the final chunk (less than 10 transactions)
            if chunk:
                self._display_table(f"Saved Transactions (Page {count//10 + 1})", chunk)

    def delete_transaction(self):
        if not self.transactions:
            CONSOLE.print("[yellow]Nothing to delete in pending list[/yellow]")
            return
        self.list_transactions()
        idx = Prompt.ask("Enter ID to delete", default="0")
        try:
            index = int(idx) - 1
            if 0 <= index < len(self.transactions):
                update_user_balance(
                    self.user, self.transactions[index].amount, self.transactions[index].type, -1)
                del self.transactions[index]
                CONSOLE.print("[bold green]Deleted successfully[/bold green]")
            else:
                CONSOLE.print("[bold red]Invalid ID[/bold red]")
        except ValueError:
            CONSOLE.print("[bold red]Please enter a number[/bold red]")

    def save_transactions(self):
        if not self.transactions:
            return
        with open(DATAFILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for t in self.transactions:
                writer.writerow([t.date, t.amount, t.type, t.category, t.description])
        self.transactions.clear()
        CONSOLE.print("[bold blue]Data saved to transactions.csv[/bold blue]")


def percentage(amount, total):
    return (amount / total * 100) if total != 0 else 0


def update_user_balance(user, amount, type, coefficient):
    # coefficient: 1 (add) or -1 (delete)
    if type == "income":
        user.income += int(amount) * coefficient
    else:
        user.expenses += int(amount) * coefficient


def data_validation():
    with open(DATAFILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != HEADER:
            return False
        for row in reader:
            if len(row) != len(HEADER) or not Transaction(*row).validate():
                return False
    return True


def view_statistics(new_pending):
    stats = {cat: 0 for cat in AVAILABLE_CATEGORIES}
    total_expense = 0

    def process_row(amount, type, category):
        nonlocal total_expense
        if type == "expense":
            stats[category] += int(amount)
            total_expense += int(amount)

    for t in new_pending:
        process_row(t.amount, t.type, t.category)

    with open(DATAFILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            process_row(row[1], row[2], row[3])

    table = Table(title="[bold]EXPENSE ANALYSIS BY CATEGORY[/bold]", border_style="blue")
    table.add_column("Category", style="cyan")
    table.add_column("Amount", justify="right", style="bold red")
    table.add_column("Percentage", justify="right", style="green")

    for cat, amt in stats.items():
        if amt > 0:
            pct = percentage(amt, total_expense)
            table.add_row(cat, f"{amt:,}", f"{pct:.1f}%")

    CONSOLE.print(table)
    CONSOLE.print(Panel(f"Total Expense: [bold red]{total_expense:,}[/bold red]", expand=False))


def main():
    if not os.path.exists(DATAFILE):
        with open(DATAFILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
    elif not data_validation():
        CONSOLE.print(
            Panel("[bold red]Error:[/bold red] transactions.csv is corrupted!", title="System"))
        sys.exit(1)

    user = User()
    history = NewTransactionHistory(user)

    while True:
        menu = Panel(
            "[1] [bold]Transaction[/bold] (Add/List/Del)\n"
            "[2] [bold]Categories[/bold]\n"
            "[3] [bold]Statistics[/bold]\n"
            "[4] [bold red]Exit & Save[/bold red]",
            title="[bold green]PERSONAL FINANCE TRACKER[/bold green]",
            subtitle=f"[bold]Balance: {user.income - user.expenses:,}[/bold]",
            expand=False
        )
        CONSOLE.print(menu)

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            while True:
                CONSOLE.print("\n[bold]1.1 Add | 1.2 List | 1.3 Delete | 1.4 Back[/bold]")
                sub_choice = Prompt.ask("Sub-menu", choices=["1", "2", "3", "4"])
                if sub_choice == "1":
                    history.add_transaction()
                elif sub_choice == "2":
                    history.list_transactions()
                elif sub_choice == "3":
                    history.delete_transaction()
                else:
                    break
        elif choice == "2":
            cols = Columns([Panel(cat, expand=True) for cat in AVAILABLE_CATEGORIES], equal=True)
            CONSOLE.print(Panel(cols, title="Available Categories"))
        elif choice == "3":
            view_statistics(history.transactions)
        elif choice == "4":
            history.save_transactions()
            CONSOLE.print("[italic]Exiting... Goodbye![/italic]")
            break


if __name__ == "__main__":
    main()
