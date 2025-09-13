from business_logic import entities, services, validation
from data_access import repositories
from presentation import controller, ui_components


def main():
    # Check for the existence of the database, if not, initialize it
    repositories.initialize_database()

    # Repositories
    transaction_repo = repositories.TransactionRepository()
    category_repo = repositories.CategoryRepository()

    # Entities
    user = entities.User(transaction_repo.readall())
    categories = entities.Categories(category_repo.readall())

    # Validation
    transaction_validation = validation.TransactionValidation(category_repo.readall())

    # Services
    user_service = services.UserService(user)
    transaction_service = services.TransactionService(transaction_repo)

    # Controller
    backend_controller = controller.Controller(
        transaction_repo,
        category_repo,
        categories,
        user,
        transaction_validation,
        user_service,
        transaction_service,
    )

    # Run
    app = ui_components
    app.run_application(backend_controller)


if __name__ == "__main__":
    main()
