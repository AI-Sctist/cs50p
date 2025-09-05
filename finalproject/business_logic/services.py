import entities


class UserService:
    """
    Change user's income and expense according to the info of the transaction created or
    deleted by user
    """

    def __init__(self, user):
        self.user = user

    def apply_transaction(self, type, amount):
        if type == "income":
            self.user._income += amount
        elif type == "expense":
            self.user._expense += amount
        else:
            raise ValueError(f"Unknown transaction type: {type}")

    def revert_transaction(self, type, amount):
        if type == "income":
            self.user._income -= amount
        elif type == "expense":
            self.user._expense -= amount
        else:
            raise ValueError(f"Unknown transaction type: {type}")


class TransactionService:
    def __init__(self, validation, transaction_repository):
        self.validation = validation
        self.data_access = transaction_repository

        self.id_digit_amount = 9

    def create(self, user, **kwargs):
        # Generate transaction id using auto-increment (transaction count)
        transaction = entities.Transaction(
            f"{user.transaction_amount:0{self.id_digit_amount}d}", **kwargs
        )

        self.validate(**transaction.__dict__)
        self.data_access.create(transaction.__dict__)

    def readall(self):
        return self.data_access.readall()

    def update(self, id, **kwargs):
        # Data_access will raise TypeError if some kwargs don't exist
        self.validate(**kwargs)
        self.data_access.update(id, kwargs)

    def delete(self, id):
        """
        Delete a specified transaction and return a dict(type, amount) for UserService
        """
        return self.data_access.delete(id)

    # Add some filters by transaction fields (filter txn history)
    ...

    # Add sort by transaction fields
    ...

    def validate(self, **kwargs):
        """
        Supported kwargs is the fields of a transaction (see Transaction entity)
        """

        # iterate and normalize and check (delete this after implement)
        for key, value in kwargs.items():
            match key:
                case "id":
                    if not isinstance(value, str):
                        raise TypeError("Transaction id must be str")
                    else:
                        value = value.strip().lower()
                        if not (
                            len(value) == self.id_digit_amount and value.isnumeric()
                        ):
                            return False
                case "type":
                    if not isinstance(value, str):
                        raise TypeError("transaction type must be str")
                    else:
                        value = value.strip().lower()
                        if not self.validation.type_validate(value):
                            return False
                case "amount":
                    if not isinstance(value, int):
                        raise TypeError("Transaction amount must be int")
                    else:
                        if not self.validation.amount_validate(value):
                            return False
                case "date_time":
                    if not isinstance(value, str):
                        raise TypeError("Transaction date_time must be str")
                    else:
                        value = value.strip().lower()
                        if not self.validation.date_time.validate(value):
                            return False
                case "category":
                    if not isinstance(value, str):
                        raise TypeError("Transaction category must be str")
                    else:
                        value = value.strip().lower()
                        if not self.validation.category_validate(value):
                            return False
                case "note":
                    if not isinstance(value, str):
                        raise TypeError("Transaction note must be str")
                    else:
                        value = value.strip()
                        # note can be empty, so no need to validate
                case _:
                    raise ValueError("Unknown keyword argument: {key}")

        return True  # Pass all tests
