class Transaction:
    """
    Contains the attributes of a transaction. Can only be changed via the service module
    for data validation
    """
    def __init__(self, type, amount, date_time, category, note):
        self._type = type
        self._amount = amount
        self._date_time = date_time
        self._category = category
        self._note = note

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
    """
    def __init__(self, categories):
        self.categories = {}
        self.categories.update(categories)

    def create(self, category):
        self.categories.add(category)

    def delete(self, category):
        self.categories.discard(category)

class User:
    """
    Contains the user's income and expense. Can only be changed via the service module
    """
    def __init__(self, transaction_history):
        self._income = 0
        self._expense = 0

        for transaction in transaction_history:
            if transaction.type == "income":
                self._income += transaction.amount
            else:
                self._expense += transaction.amount

    @property
    def income(self):
        return self._income
    
    @property
    def expense(self):
        return self._expense
    
    @property
    def balance(self):
        return self.income - self.expense
