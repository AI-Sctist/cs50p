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
            pen = csv.DictWriter(file, fieldnames=TransactionRepository.FIELDNAMES)
            pen.writerow(transaction)

    def read_all(self):
        with open(self.file_path, "r", newline="") as file:
            for transaction in csv.DictReader(file):
                yield transaction

    def update(self, id, **kwargs):
        # Helper function for changing data fields
        def change(transaction):
            for key, value in kwargs.items():
                transaction[key] = value

        # Temporary store data
        with open(self.file_path, "r", newline="") as src, open(
            self.tmp,
            "w",
            newline="",
        ) as dst:
            pen = csv.DictWriter(dst, fieldnames=TransactionRepository.FIELDNAMES)
            for transaction in csv.DictReader(src):
                if transaction["id"] == id:
                    change(transaction)
                pen.writerow(transaction)

        # Write to src file
        os.replace(self.tmp, self.file_path)

    def delete(self, id):
        # Temporary store data
        with open(self.file_path, "r", newline="") as src, open(
            self.tmp,
            "w",
            newline="",
        ) as dst:
            pen = csv.DictWriter(dst, fieldnames=TransactionRepository.FIELDNAMES)
            for transaction in csv.DictReader(src):
                if transaction["id"] != id:
                    pen.writerow(transaction)

        # Write to src file
        os.replace(self.tmp, self.file_path)


class CategoryRepository:
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

    def read_all(self):
        with open(self.file_path, "r") as file:
            for category in file:
                yield category.strip()

    def delete(self, name):
        # Temporary store data
        with open(self.file_path, "r") as src, open(self.tmp, "w") as dst:
            for category in src:
                if category.strip() != name.strip():
                    dst.write(category + "\n")

        # Write to src file
        os.replace(self.tmp, self.file_path)
