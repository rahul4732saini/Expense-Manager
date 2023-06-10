r"""
Module related to functions required for the
management and troubleshooting of transactions.

This exports:

(Class) Manage:
---------------
-   get_transactions_id: returns a list transactions ID.
-   get_transactions: return a list of all existing valid transactions in the form of dictionaries.
-   add_transaction: used to create a new transaction.
-   switch_transaction: used to switch transaction status between upcoming - cleared - cancelled.
-   edit_transaction: used to edit the details of the transaction corresponding to the transaction ID provided.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")
    
    import pickle
    import random
    import datetime
    import data.info as info
    from threading import Thread
    from common.objects import Transaction, Transactions
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_transactions(self) -> Transactions:

        # Capturing transaction from the data folder.
        try:
            with open(info.DATA_TRANSACTIONS, 'r') as file:
                    transactions: Transactions = pickle.load(file)

                    assert transactions.__class__ == Transactions
        except Exception:
            raise Exception()
        
        return transactions

    def _create_transaction_id(self) -> None:
        # The max length of the ID is 10 digits.
        transaction_id: str = str(random.randrange(1,10**10))
        
        # While loop is called to define another ID if the ID generated already exists.
        while transaction_id in self.get_transactions_id():
            transaction_id: str = str(random.randrange(1,10**10))

        # Changes the length of the ID by adding 0s in the begining if the length is less than 10.
        transaction_id = "%s%s" % ("0"*(10-transaction_id.__len__()),transaction_id) if transaction_id.__len__() < 10 else transaction_id
        self._transaction_id: str = transaction_id

    def write_transaction(self, transactions: Transactions) -> None:
        assert transactions.__class__ == Transactions, ""

        with open(info.DATA_TRANSACTIONS, 'w') as file:
            pickle.dump(transactions, file)

    def add_transaction(self,
                        amount: int | float,
                        transaction_type: str,
                        payment_mode: str,
                        catagory: str | dict,
                        transaction_datetime: datetime.datetime,
                        description: str = None) -> None:
        
        # Creating an unique transaction ID
        thread = Thread(self._create_transaction_id(), daemon = True)
        thread.start()

        if not hasattr(self, "_transaction_id"):
            raise Exception("0xetrn0007")
        
        entry: Transaction = Transaction(
            transaction_id = self._transaction_id,
            datetime_added = datetime.datetime.today(),
            status = "cleared",
            amount = amount,
            transaction_type = transaction_type,
            payment_mode = payment_mode,
            catagory = catagory,
            transaction_datetime = transaction_datetime,
            description = description
        )

        transactions: Transactions = self.get_transactions()
        transactions.transactions.append(entry)

        self.write_transaction(transactions)

    def switch_transaction(self, transaction: Transaction) -> None:
        transaction.status = "cleared" if transaction.status == "cleared" else "cancelled"

    def edit_transaction(self,
                        transaction_id: str,
                        amount: int | float = None,
                        transaction_type: str = None,
                        payment_mode: str = None,
                        catagory = None,
                        transaction_datetime: datetime.datetime = None,
                        description: str = None) -> None:

        # Dictionary of the edits to be updated in the transaction.
        edit: dict = {key: value for key, value in locals().items() if value != None and key not in ["self", "transaction_id"]}

        if edit.__len__() == 0:
            raise Exception("0xetrn0012")

        # Iterates through the transactions and checks if a transaction exists with the provided transaction ID.
        # Raises an error if no corresponding transaction is found.
        i: dict
        for i in self.get_transactions():
            if i["transaction_id"] == transaction_id:
                transaction: dict = i
                break
        else:
            raise Exception("0xetrn0006")

        # Updating the transaction and saving it to the transaction file.
        transaction.update(edit)
        self.write_transaction(transaction, exists = True)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    def er_0xetrn0001(self) -> bool:
        ...
        
    def er_0xetrn0002(self) -> bool:
        ...

    def er_0xetrn0003(self) -> bool:
        ...

    def er_0xetrn0004(self) -> bool:
        ...

    def er_0xetrn0006(self) -> bool:
        ...

    # pending...