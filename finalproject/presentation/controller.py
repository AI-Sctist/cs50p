class Controller:
    def __init__(
        self,
        transaction_manager,
        category_manager,
        category,
        user,
        transaction_validation,
        user_service,
        transaction_service,
    ):
        # Data access
        self.transaction_manager = transaction_manager
        self.category_manager = category_manager

        # Entities
        self.category = category
        self.user = user

        # Validation
        self.transaction_validation = transaction_validation

        # Services
        self.user_service = user_service
        self.transaction_service = transaction_service

    def get_income(self):
        return self.user.income

    def get_expense(self):
        return self.user.expense

    def get_balance(self):
        return self.user.balance

    def save_transaction(self, **kwargs):
        self.transaction_validate(**kwargs)
        self.transaction_service.create(self.user, **kwargs)
        self.user_service.apply_transaction(kwargs["type"], int(kwargs["amount"]))

    def update_transaction(self, id, **kwargs):
        self.transaction_validate(**kwargs)
        if (
            transaction_info := self.transaction_service.update(id, **kwargs)
        ) is not None:
            self.user_service.apply_transaction(
                transaction_info["type_old"],
                int(transaction_info["amount_old"]),
                transaction_info["type_new"],
                int(transaction_info["amount_new"]),
            )

    def delete_transaction(self, id):
        if (transaction_info := self.transaction_service.delete(id)) is not None:
            self.user_service.revert_transaction(
                transaction_info["type"], int(transaction_info["amount"])
            )

    def get_all_transactions(self):
        return self.transaction_service.readall()

    def transaction_validate(self, **kwargs):
        """
        Remember: all data are in string format when received from UI
        """

        for field, value in kwargs.items():
            match field:
                case "type":
                    if not self.transaction_validation.type_validate(value):
                        raise ValueError(f"Invalid type: {value}")
                case "amount":
                    if not self.transaction_validation.amount_validate(value):
                        raise ValueError(f"Invalid amount: {value}")
                case "category":
                    if not self.transaction_validation.category_validate(value):
                        raise ValueError(f"Invalid category: {value}")
                case "date_time":
                    if not self.transaction_validation.date_time_validate(value):
                        raise ValueError(f"Invalid date and time: {value}")
                case "note":
                    # Note can be any string, no validation needed
                    pass
                case _:
                    raise ValueError(f"Unknown field: {field}")

    def filter_by(self, fieldname, *args):
        """
        args usage depends on fieldname:
        "category": <category>
        "type": <type>
        "date_time": <start_date>, <end_date>
        "amount": <min_amount>, <max_amount>
        """

        match fieldname:
            case "category":
                return self.transaction_service.filter_by_category(*args)
            case "type":
                return self.transaction_service.filter_by_type(*args)
            case "date_time":
                return self.transaction_service.filter_by_date_range(*args)
            case "amount":
                return self.transaction_service.filter_by_amount_range(*args)
            case _:
                raise ValueError(f"Not support fieldname: {fieldname}")

    def stats_expense_by_category(self):
        """
        Return dict(category: <total_expense>) and total(for percentage calculation)
        """

        stats = {}
        total = 0
        for category in self.category.categories:
            stats[category] = 0

        for transaction in self.transaction_service.filter_by_type("expense"):
            total += int(transaction["amount"])
            stats[transaction["category"]] += int(transaction["amount"])

        return stats, total

    # Income by category not promised feature :))
    # Give me money first (-_-)

    def get_categories(self):
        return list(self.category.categories)

    def add_category(self, category):
        # Database
        if category not in self.category.categories:
            self.category_manager.create(category)

        # State
        self.category.create(category)

    def remove_category(self, category):
        # Database
        self.category_manager.delete(category)

        # State
        self.category.delete(category)
