import datetime


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
