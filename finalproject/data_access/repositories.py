import csv
import os


class TransactionRepository:
    FIELDNAMES = ["id", "type", "amount", "date_time", "category", "note"]

    def __init__(self):
        # Get database root path
        current_folder = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(current_folder)
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
        Return a dict(type_old, amount_old, type_new: amount_new) of the transaction for
        calculating user's balance
        """

        # Helper function for changing data fields
        def change(transaction):
            for key, value in kwargs.items():
                transaction[key] = value

        # Return data
        return_data = None

        # Temporary store data
        with open(self.file_path, "r", newline="") as src, open(
            self.tmp,
            "w",
            newline="",
        ) as dst:
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
        Delete a transaction in the database, return a dict(type, amount) of the transaction
        for calculating user's balance
        """

        # Return data
        return_data = None

        # Temporary store data
        with open(self.file_path, "r", newline="") as src, open(
            self.tmp,
            "w",
            newline="",
        ) as dst:
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
        current_folder = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(current_folder)
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


def initialize_database():
    def write_header():
        with open(transactions, "w", newline="") as file:
            csv.DictWriter(
                file,
                fieldnames=TransactionRepository.FIELDNAMES,
            ).writeheader()

    # Project root
    parent = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(parent)

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
                != TransactionRepository.FIELDNAMES
            ):
                write_header()

    # Initialize default categories
    categories = os.path.join(database, "categories.txt")
    if not os.path.exists(categories) or os.path.getsize(categories) == 0:
        with open(categories, "w") as file:
            for cat in CategoryRepository.DEFAULT:
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