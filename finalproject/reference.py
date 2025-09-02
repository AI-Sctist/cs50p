import csv
import customtkinter
import datetime
import matplotlib
import re
import sys

# OUR GODDDD
# print(customtkinter.CTkFont(family="", size=).measure(""))


def today():
    return datetime.date.today().isoformat()


class Transaction:
    def __init__(self, type, amount, category, date, note, category_manager):
        # For cheking valid category
        self._category_manager = category_manager

        self.type = type.strip().lower()
        self.amount = int(amount)
        self.category = category.strip().lower()
        self.date = date.strip().lower()
        self.note = note.strip().lower()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in ["income", "expense"]:
            raise ValueError("Invalid type")
        else:
            self._type = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in self._category_manager.categories:
            raise ValueError("Invalid category")
        else:
            self._category = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if match := re.fullmatch(r"(\d{4}-\d{2}-\d{2})", value):
            try:
                datetime.strptime(value, r"%Y-%m-%d")
            finally:
                self._date = value
        else:
            raise ValueError("Invalid date")


class CategoryManager:
    # Default categories (refer to MoneyNote app)
    categories = {
        "food",
        "houseware",
        "clothes",
        "cosmetic",
        "exchange",
        "medical",
        "education",
        "electric bill",
        "transportation",
        "contact fee",
        "housing expense",
    }

    def __init__(self, transaction_history):
        self.categories.update(row[2] for row in transaction_history)

    def add_category(self, name):
        self.categories.add(name.strip().lower())

    def remove_category(self, name):
        self.categories.remove(name.strip().lower())

    def title(self):
        return {category.title() for category in self.categories}


class TransactionManager:
    def __init__(self):
        self._expense = self._income = 0
        self._history = []

        try:
            with open("data.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                self._history = list(reader)
        except FileNotFoundError:
            GUI.report_error()
            sys.exit("Not found the data.csv file")

        for transaction in self._history:
            if transaction["type"] == "income":
                self._income += int(transaction["amount"])
            else:
                self._expense += int(transaction["amount"])

    def add_transaction(self, transaction):
        if transaction.type == "income":
            self._income += int(transaction.amount)
        else:
            self._expense += int(transaction.amount)

        self._history.append(transaction.__dict__)

    def delete_transaction(self, index):
        if self._history[index]["type"] == "income":
            self._income -= self._history[index]["amount"]
        else:
            self._expense -= self._history[index]["amount"]

        self._history[index:index+1] = []

    def save_data(self):
        try:
            with open("data.csv", "w", newline="") as file:
                pen = csv.DictWriter(file)
                pen.writerows(self._history)
        except FileNotFoundError:
            GUI.report_error()
            sys.exit("Not found the data.csv file")

    @property
    def history(self):
        return self._history

    @property
    def income(self):
        return self._income

    @property
    def expense(self):
        return self._expense
    
    @property
    def balance(self):
        return self._income - self._expense


class GUI:
    def __init__(self, transaction_manager, category_manager):
        # Passing reference
        self.transaction = transaction_manager
        self.cat = category_manager

        # Runner
        self.create_new_window()
        self.create_tabview()
        self.create_dashboard_tab()
        self.create_transaction_tab()
        self.create_history_tab()

    def create_new_window(self):
        # Create a new window
        self.window = customtkinter.CTk()
        self.window.title("Personal Financial transaction")
        self.window.geometry("722x490")

        # Block resize (support later)
        self.window.resizable(False, False)

    def create_tabview(self):
        # Set up tabview
        tabview = customtkinter.CTkTabview(
            self.window,
            width = 702,
            height = 480,
            fg_color = "#1a1f35",
            corner_radius = 20,
            border_width = 3,
            segmented_button_selected_hover_color = "#304489",
            segmented_button_selected_color = "#304489",
        )

        # Increase tab bar size
        tabview._segmented_button.configure(font=("Roboto Medium", 14))

        # Add options
        self.dashboard_tab = tabview.add("Dashboard")
        self.transaction_tab = tabview.add("Transaction")
        self.history_tab = tabview.add("History")

        # Show tabview
        tabview.grid(row=0, column=0, padx=10)

    def create_dashboard_tab(self):
        def create_balance_display():
            # Set up label
            label = customtkinter.CTkLabel(
                master = self.dashboard_tab,
                height = 15,
                text = "Current Balance",
                text_color = "#9fa3bc",
                font = ("Roboto Medium", 15),
            )

            # Display label
            label.grid(row=0, column=0, sticky="nw")

            # Set up balance display
            self.balance_display = customtkinter.CTkLabel(
                master = self.dashboard_tab,
                height = 25,
                text = f"{self.transaction.balance:,} VND",
                text_color = "#EF4444" if self.transaction.balance < 0 else "#22C55E",
                font = ("Roboto Medium", 25),
            )

            # Display balance
            self.balance_display.grid(row=1, column=0, sticky="nw")

        def create_pie_chart():
            # Pie chart
            ...

        def create_line_bar_chart():
            # Income and expense (bar&line chart)
            ...

        # Set up layout grid
        self.dashboard_tab.grid_rowconfigure(index=1, weight=10)
        self.dashboard_tab.grid_rowconfigure(index=2, weight=10)
        self.dashboard_tab.grid_rowconfigure(index=3, weight=57)
        self.dashboard_tab.grid_columnconfigure(index=0, weight=1)
        self.dashboard_tab.grid_columnconfigure(index=1, weight=1)

        # Runner
        create_balance_display()
        create_pie_chart()
        create_line_bar_chart()

    def create_transaction_tab(self):
        # Transaction
        type = customtkinter.StringVar()
        amount = customtkinter.StringVar()
        category = customtkinter.StringVar()
        date = customtkinter.StringVar(value=today())
        note = customtkinter.StringVar()

        def create_savetransaction_button():
            def save_transaction():
                self.transaction.add_transaction(Transaction(
                    type.get(),
                    amount.get(),
                    category.get(),
                    date.get(),
                    note.get(),
                ))

            # Set up save button
            save_button = customtkinter.CTkButton(
                master = self.transaction_tab,
                height = 47,
                corner_radius = 12,
                fg_color = "#4f84f6",
                text_color = "#eaeeef",
                text = "Save Transaction",
                font = ("Roboto Medium", 20),
                command = save_transaction,
            )

            # Display save button
            save_button.grid(row=5, column=0, columnspan=2)

        def create_label(txt, rw):
            """Helper function for creating transaction field labels."""
            label = customtkinter.CTkLabel(
                master = self.transaction_tab,
                text = txt,
                text_color = "#d3d7e2",
                font = ("Roboto Medium", 17.5),
            )

            label.grid(
                row=rw, column=0, sticky="w", padx=(15, 0)
            )

        def create_type_segmented_button():
            # Label field
            create_label("Transaction Type", 0)

            ## Set up radio buttons
            self.type_segmentedbutton = customtkinter.CTkSegmentedButton(
                master = self.transaction_tab,
                width = 60,
                height = 42,
                corner_radius = 17,
                border_width = 3,
                selected_color = "#527ff5",
                selected_hover_color = "#527ff5",
                unselected_color = "#2c2f40",
                unselected_hover_color = "#2c2f40",
                text_color = "#b8ceef",
                font = ("Roboto Medium", 16),
                values = ["Income", "Expense"],
                variable = type,
            )

            # Display segmented button
            self.type_segmentedbutton.grid(row=0, column=1, sticky="w")

        def create_amount_entry():
            # Label field
            create_label("Amount", 1)

            # Set up money entry
            self.amount_entry = customtkinter.CTkEntry(
                master = self.transaction_tab,
                textvariable = amount,
                height = 47,
                corner_radius = 12,
                fg_color = "#2d3041",
                text_color = "#d2d3d9",
                placeholder_text_color = "#8c90a4",
                placeholder_text = "VND",
                font = ("Roboto Medium", 16),
            )

            # Display money entry
            self.amount_entry.grid(row=1, column=1, sticky="ew")

        def create_category_optionmenu():
            # Label field
            create_label("Category", 2)

            # Set up category option menu
            self.category_optionmenu = customtkinter.CTkOptionMenu(
                master = self.transaction_tab,
                height = 47,
                corner_radius = 12,
                fg_color = "#2d3041",
                button_color = "#2d3041",
                dropdown_fg_color = "#2d3041",
                text_color = "#d2d3d9",
                font = ("Roboto Medium", 16),
                dropdown_font = ("Roboto Medium", 16),
                hover = False,
                values = list(self.cat.categories) + ["Other"],
                variable = category,
            )

            # Display category option menu
            self.category_optionmenu.grid(row=2, column=1, sticky="ew")

        def create_date_entry():
            # Label field
            create_label("Date", 3)

            self.date_entry = customtkinter.CTkEntry(
                master = self.transaction_tab,
                textvariable = date,
                height = 47,
                corner_radius = 12,
                fg_color = "#2d3041",
                text_color = "#d2d3d9",
                placeholder_text_color = "#8c90a4",
                font = ("Roboto Medium", 16),
            )

            # Display money entry
            self.date_entry.grid(row=3, column=1, sticky="ew")

        def create_note_entry():
            # Label field
            create_label("Note", 4)

            # Set up note entry
            self.note_entry = customtkinter.CTkEntry(
                master = self.transaction_tab,
                textvariable = note,
                height = 47,
                corner_radius = 12,
                fg_color = "#2d3041",
                text_color = "#d2d3d9",
                placeholder_text_color = "#8c90a4",
                placeholder_text = "*optional",
                font = ("Roboto Medium", 16),
            )

            # Display note entry
            self.note_entry.grid(row=4, column=1, sticky="ew")

        ## Set up layout grid
        self.transaction_tab.grid_rowconfigure(index=0, weight=27)
        for i in range(1, 5):
            self.transaction_tab.grid_rowconfigure(index=i, weight=27)
        self.transaction_tab.grid_rowconfigure(index=5, weight=48)
        
        self.transaction_tab.grid_columnconfigure(index=0, weight=2)
        self.transaction_tab.grid_columnconfigure(index=1, weight=23)

        # Runner
        create_type_segmented_button()
        create_amount_entry()
        create_category_optionmenu()
        create_date_entry()
        create_note_entry()
        create_savetransaction_button()


    def create_history_tab(self):
        # Executable class

        # Some functions here
        ...

        ## Set up layout grid
        ...

        ...

        # Runner
        ...

    def report_error():
        # Error: not found data.csv when init TransactionManager
        ...


def main():
    # Initialize Back-end
    transaction_manager = TransactionManager()
    category_manager = CategoryManager(transaction_manager.history)

    # Initialize Front-end
    app = GUI(transaction_manager, category_manager)

    # Run app
    app.window.mainloop()
