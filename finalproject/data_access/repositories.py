import csv
import os


class TransactionRepository:
    def __init__(self):
        # Get project root path
        current_folder = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(current_folder)
        database = os.path.join(root, "database")

        # Access database
        self.file_path = os.path.join(database, "transactions.csv")

        # Temporary files
        self.txt_tmp = os.path.join(database, "temporary_files", "tmp.txt")
        self.csv_tmp = os.path.join(database, "temporary_files", "tmp.csv")

    def get_all_transactions(self):
        with open(self.file_path, "r", newline="") as file:
            for transaction in csv.DictReader(file):
                yield transaction

    def add_transaction(self, transaction):
        with open(self.file_path, "a", newline="") as file:
            pen = csv.DictWriter()
            pen.writerow(transaction)


class CategoryRepository:
    ...
