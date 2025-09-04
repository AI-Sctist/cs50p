import datetime


class TransactionValidation:
    """
    If we have a complete transaction obj, use overall_validate is faster, but if we want
    to specify some attributes, use single instead, or we can create a formal object and
    modified it
    """

    def __init__(self, categories):
        self.defined_categories = categories # Store state, so use class

    def type_validate(self, value):
        return value in ["income", "expense"]

    def amount_validate(self, value):
        return value > 0

    def date_time_validate(self, value):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    def category_validate(self, value):
        return value in self.defined_categories

    def overall(self, transaction):
        return (
            self.type_validate(transaction.type)
            and self.amount_validate(transaction.amount)
            and self.date_time_validate(transaction.date_time)
            and self.category_validate(transaction.category)
        )
