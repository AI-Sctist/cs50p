import business_logic
import data_access


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

    def get_categories(self):
        return list(self.category.categories)

    def save_transaction(self, **kwargs):
        self.transaction_service.create(self.user, **kwargs)
