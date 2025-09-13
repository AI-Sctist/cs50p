from business_logic import entities


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
