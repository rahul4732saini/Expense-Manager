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
    
    import re
    import random
    import datetime
    import data.info as info
    from threading import Thread
    from common.directory import Indexer
    import data.pre_requisites as pre_requisites
    import transactions.payment_mode as pay_mode
    from transactions.catagory import Income, Expense
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_transactions_id(self) -> list[str]:

        # Capturing transaction files from the transactions data folder.
        try:
            transaction_files: list[str] = Indexer(info.DATA_TRANSACTIONS).get_files()
        except Exception:
            raise Exception("0xetrn0004")

        # Verifying the names of the transaction files.
        i: str
        for i in transaction_files:
            if not re.match("^trn_id_[0-9]{10}.txt$", i):
                raise Exception("0xetrn0001")

        # Returning only the ID of the transactions as strings.
        return [i[7:-4] for i in transaction_files]

    def _create_transaction_id(self) -> None:
        # The max length of the ID is 10 digits.
        transaction_id: str = str(random.randrange(1,10**10))
        
        # While loop is called to define another ID if the ID generated already exists.
        while transaction_id in self.get_transactions_id():
            transaction_id: str = str(random.randrange(1,10**10))

        # Changes the length of the ID by adding 0s in the begining if the length is less than 10.
        transaction_id = "%s%s" % ("0"*(10-transaction_id.__len__()),transaction_id) if transaction_id.__len__() < 10 else transaction_id
        self._transaction_id: str = transaction_id

    def _verify_transaction(self, trn: dict, exists: bool) -> None:
        # transaction_dictionary as namespace trn

        try:
            if not all(
                (
                    # Verifying transaction_ID
                    trn["transaction_id"] in self.get_transactions_id() if exists else re.match("^[0-9]{10}$", trn["transaction_id"]),

                    # Verifying datetime_added
                    trn["datetime_added"].__class__ == datetime.datetime and trn["datetime_added"].year <= datetime.datetime.today().year,

                    trn["status"] in pre_requisites.TRANSACTION_STATUS, # Verifying status
                    trn["amount"].__class__ in [int, float] and trn.get("amount") > 0, # Verifying transaction_amount
                    trn["transaction_type"] in pre_requisites.TRANSACTION_TYPES, # Verifying transaction_type
                    trn["payment_mode"] in pay_mode.Manage().get_mode_names(), # Verifying payment_mode

                    # Verifying catagory
                    trn["catagory"].__class__ == str,
                    trn["catagory"] in list((Income() if trn["transaction_type"] == "income" else Expense()).get_catagories().keys()) + [None],

                    # Verifying transaction_datetime
                    trn["transaction_datetime"].__class__ == datetime.datetime and trn["transaction_datetime"].year in range(1980, 2100),

                    # Verifying description
                    trn["description"] == None or trn["description"].__class__ == str and trn["description"].__len__() <= 100
                )
            ):
                raise Exception
        except Exception:
            raise Exception("0xetrn0008")

    def get_transactions(self) -> list[dict]:
        transactions_id: list[str] = self.get_transactions_id()
        transactions: list[dict] = list()

        # Accessing the transaction files, capturing the transactions and verifying them.
        i: str
        for i in transactions_id:
            with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, i), 'r') as file:
                try:
                    content: dict = eval(file.read())
                    self._verify_transaction(content, exists = True)

                    # Checking for invalid transaction_ID(s).
                    if content["transaction_id"] != i:
                        raise Exception
                except Exception:
                    raise Exception("0xetrn0003")
                
                transactions.append(content)

        return transactions

    def write_transaction(self, transaction: dict, exists: bool) -> None:

        # Verifying the transaction.
        self._verify_transaction(transaction, exists)

        # Converting the transaction dictionary into a readable string format to be written in the file.
        with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, transaction["transaction_id"]), 'w') as file:
            file.write(str(transaction).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}"))

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
        
        entry: dict = {
            "transaction_id": self._transaction_id,
            "datetime_added": datetime.datetime.today(),
            "status": "cleared",
            "amount": amount,
            "transaction_type": transaction_type,
            "payment_mode": payment_mode,
            "catagory": catagory,
            "transaction_datetime": transaction_datetime,
            "description": description
        }

        self.write_transaction(entry, exists = False)

    def switch_transaction(self, transaction_id: str) -> None:

        # Iterates through the transactions and checks if a transaction exists with the provided transaction ID.
        # Raises an error if no corresponding transaction is found.
        i: dict
        for i in self.get_transactions():
            if i["transaction_id"] == transaction_id:
                transaction: dict = i
                break
        else:
            raise Exception("0xetrn0005")

        # Changing the transaction's status, and saving it into the transaction file
        transaction.update({"status": "cleared" if transaction["status"] == "cancelled" else "cancelled"})
        self.write_transaction(transaction, exists = True)

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