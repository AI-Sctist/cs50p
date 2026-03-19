import os
import csv

from rich import print
from rich.console import Console

import project

CONSOLE = Console()
project.DATAFILE = "test_transactions.csv"


def test_percentage_normal_case():
    assert project.percentage(50, 100) == 50


def test_percentage_zero_total():
    assert project.percentage(0, 0) == 0


def test_update_user_balance_addition():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 50000, 'expense', 'food', 'Breakfast Banh Mi'])
        writer.writerow(['2026-03-01', 15000000, 'income', 'other', 'Monthly Salary'])
        writer.writerow(['2026-03-02', 45000, 'expense', 'transportation', 'Bus fare'])

    user = project.User()
    income = user.income
    expenses = user.expenses

    project.update_user_balance(user, 10000, 'income', 1)
    project.update_user_balance(user, 5000, 'expense', 1)

    assert user.income == income + 10000
    assert user.expenses == expenses + 5000


def test_update_user_balance_deletion():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 50000, 'expense', 'food', 'Breakfast Banh Mi'])
        writer.writerow(['2026-03-01', 15000000, 'income', 'other', 'Monthly Salary'])
        writer.writerow(['2026-03-02', 45000, 'expense', 'transportation', 'Bus fare'])

    user = project.User()
    income = user.income
    expenses = user.expenses

    project.update_user_balance(user, 10000, 'income', -1)
    project.update_user_balance(user, 5000, 'expense', -1)

    assert user.income == income - 10000
    assert user.expenses == expenses - 5000


def test_data_validation_missing_header():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Category', 'Description'])

    assert project.data_validation() == False


def test_data_validation_wrong_header():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Categories', 'Descriptions'])

    assert project.data_validation() == False


def test_data_validation_wrong_date_format():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['03-01-2026', 50000, 'expense', 'food', 'Breakfast Banh Mi'])

    assert project.data_validation() == False


def test_data_validation_wrong_amount_format():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 'fifty thousand', 'expense', 'food', 'Breakfast Banh Mi'])

    assert project.data_validation() == False


def test_data_validation_wrong_type():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 50000, 'spending', 'food', 'Breakfast Banh Mi'])

    assert project.data_validation() == False


def test_data_validation_wrong_category():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 50000, 'expense', 'entertainment', 'Movie ticket'])

    assert project.data_validation() == False


def test_data_validation_valid_data():
    with open(project.DATAFILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Amount', 'Type', 'Category', 'Description'])
        writer.writerow(['2026-03-01', 50000, 'expense', 'food', 'Breakfast Banh Mi'])

    assert project.data_validation() == True


def main():
    test_percentage_normal_case()
    test_percentage_zero_total()
    test_update_user_balance_addition()
    test_update_user_balance_deletion()
    test_data_validation_missing_header()
    test_data_validation_wrong_header()
    test_data_validation_wrong_date_format()
    test_data_validation_wrong_amount_format()
    test_data_validation_wrong_type()
    test_data_validation_wrong_category()
    test_data_validation_valid_data()
    CONSOLE.print("[bold green]✔ All tests passed![/bold green]")

    os.remove(project.DATAFILE)


if __name__ == "__main__":
    main()
