# Personal Finance Tracker (CLI Version)
#### Video Demo: <URL [HERE](https://youtu.be/jLlIhu0PP5E?si=JukYQXjelDwNUvdI)>
#### Description:
This is a simple Python command-line app, using the 'rich' library to improve how the output looks. Regarding its operation, when the program is launched, it first checks the existence and validity of the data file (transactions.csv). Then, you will have a menu to navigate the program. With the Transactions option, you can add new transactions, list transactions (including previous transactions and newly added but not yet saved transactions), and delete transactions (note: only newly added transactions that have not yet been saved to the data file can be deleted). With the Category option, the software will show you the categories that you can fill in when entering a new transaction. With the statistics option, the application will display a statistics table, allowing you to see the amount you spent on each category, their percentage of the total, and the total amount spent. By skillfully utilizing the rich library, the user experience with the application is enhanced many times over compared to simply "printing" on the terminal. Regarding the implementation details, I grouped the transaction attributes into the "Transaction" class, which also includes the self.validate() method to validate the transaction components. I grouped income and expenses into the "User" class, which also includes the self.load_data() function to automatically update their income and expense information from previous transaction data. I also grouped the transaction handling methods (add, list, delete) into the "NewTransactionHistory" class, which also includes a method to automatically save the transaction to a data file when the user closes the application. Importantly, whenever a user adds or deletes a transaction, I use a real-time balance update algorithm (updating immediately upon the operation) instead of rereading all the data from scratch. Besides these main classes, I also have auxiliary functions such as a percentage calculation function, a balance update function (to be called multiple times in add/delete transaction methods), and a function to check the validity of the data file to ensure the program doesn't crash, and of course, a statistics function. Note that, for simplicity, I will only check the data at the beginning of the program run. If the user tampers with the data while the program is running, I will not be responsible for any program crashes. Below is a summary of the program's main features.

## Main Features:
- **Transaction Management:**
  Add, list, and delete income or expense records directly from the terminal

- **Data Storage:**
  All transactions are saved in a 'transactions.csv' file and updated automatically

- **Input Validation:**
  Check for valid dates ('YYYY-MM-DD'), ensures amounts are positive, and restricts categories for easier management

- **Basic Analysis:**
  Show a summary of expenses by category, including totals and percentages

- **CLI Interface with Rich:**
  Use the 'rich' library to display tables and messages in a clearer, more readable way
