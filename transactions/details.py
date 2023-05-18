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
-   delete_transaction: used to delete the transactions corresponding to the transactions ID provided as str / list.
-   edit_transaction: used to edit the details of the transaction corresponding to the transaction ID provided.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")
    
    import os
    import random
    import datetime
    from typing import Union
    import data.info as info
    from threading import Thread
    import payment_mode as pay_mode
    from common.directory import Indexer
    from catagory import Income, Expense
    import data.pre_requisites as pre_requisites
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
            if i.__len__() != 21 or i[:7] != "trn_id_" or i[7:17].isdigit() == False:
                raise Exception("0xetrn0001")
            if i.removesuffix(".txt") == i:
                raise Exception("0xetrn0002")

        # Returning only the ID of the transactions as strings.
        return [i[7:i.rfind(".")] for i in transaction_files]

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
                [
                    # Verifying transaction_ID
                    trn.get("transaction_id") in self.get_transactions_id() if exists
                    else trn.get("transaction_id").__class__ == str and trn.get("transaction_id").__len__() == 10 and trn.get("transaction_id").isdigit(),

                    # Verifying datetime_added
                    trn.get("datetime_added").__class__ == datetime.datetime and trn.get("datetime_added").year <= datetime.datetime.today().year,

                    trn.get("status") in pre_requisites.TRANSACTION_STATUS, # Verifying status
                    trn.get("amount").__class__ in [int, float] and trn.get("amount") > 0, # Verifying amount
                    trn.get("transaction_type") in pre_requisites.TRANSACTION_TYPES, # Verifying transaction_type
                    trn.get("payment_mode") in pay_mode.Manage().get_mode_names(), # Verifying payment_mode
                    trn.get("catagory").__class__ in [str, dict], # Verifying catagory

                    # Verifying transaction_datetime
                    trn["transaction_datetime"] == None or trn["transaction_datetime"].__class__ == datetime.datetime and
                    trn["transaction_datetime"].year in range(1980, 2100),

                    # Verifying description
                    trn["description"] == None or trn["description"].__class__ == str and trn["description"].__len__() <= 100
                ]
            ):
                raise Exception
        except Exception:
            raise Exception("0xetrn0008")

        catagory: Union[str,dict] = trn.get("catagory")
        income_catagory: bool = trn.get("transaction_type") == "income"

        if any(
            [   
                # Verifying catagory if transaction type == "income"
                income_catagory and (catagory.__class__ == dict and catagory.get("others") == None or
                catagory.__class__ == str and catagory not in Income().get_catagories()),

                # Verifying catagory if transaction_type == "expense"
                not income_catagory and (catagory.__class__ == dict and catagory.get("others") == None or
                catagory.__class__ == str and catagory not in Expense().get_catagories()),
            ]
        ):
            raise Exception("0xetrn0009")

    def get_transactions(self) -> list[dict]:
        transaction_files: list[str] = self.get_transactions_id()
        transactions: list[dict] = list()

        # Accessing the transaction files, capturing the transactions and verifying them.
        try:
            i: str
            for i in transaction_files:
                with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, i), 'r') as file:
                    content: dict = eval(file.read().replace("\n",""))

                    self._verify_transaction(content, exists = True)
                    transactions.append(content)
        except Exception:
            raise Exception("0xetrn0003")

        return transactions

    def _write_transaction(self, transaction_dict: dict) -> None:

        # Retrieving the transaction ID to access the related transaction file.
        transaction_id: str = transaction_dict.get("transaction_id")

        # Converting the transaction dictionary into a readable string format to be written in the file.
        transaction: str = str(transaction_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")
        
        with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, transaction_id), 'w') as file:
            file.write(transaction)

    def add_transaction(self,
                        amount: Union[int, float],
                        transaction_type: str,
                        payment_mode: str,
                        catagory: Union[str, dict],
                        transaction_datetime: datetime.datetime = None,
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

        # Verifying and saving the transaction into a file.
        self._verify_transaction(entry, exists = False)
        self._write_transaction(entry)

    def switch_transaction(self, transaction_id: str) -> None:
        if transaction_id not in self.get_transactions_id():
            raise Exception("0xetrn0005")

        # Accessing the transaction file, capturing the transaction and verifying it.
        try:
            with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, transaction_id), 'r') as file:
                transaction: dict = eval(file.read().replace("\n",""))
            
            if transaction not in self.get_transactions() or transaction.get("status") not in pre_requisites.TRANSACTION_STATUS:
                raise Exception
        except Exception:
            raise Exception("0xetrn0006")

        # Changing the transaction's status
        trn_status: str = transaction.get("status")
        trn_status = "cleared" if trn_status == "cancelled" else "cancelled"

        # Updating the transaction and saving it into the transaction file
        transaction.update({"status": trn_status})
        self._write_transaction(transaction)

    def delete_transaction(self, transactions_id: Union[list[str], str]) -> None:
        if transactions_id.__class__ not in [str, list]:
            raise Exception("0xetrn0010")

        transactions_id = transactions_id if transactions_id.__class__ == list else [transactions_id]

        if len(transactions_id) > len(self.get_transactions_id()):
            raise Exception("0xetrn0010")

        # List of transactions_id queued for deletion that exist, i.e., are valid.
        valid_transactions_id = [i for i in transactions_id if i in self.get_transactions_id()]

        # Deleting transaction files with related transactions_id.
        i: str
        for i in valid_transactions_id:
            try:
                os.remove("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, i))
            except Exception:
                os.system("del \"%s\\trn_id_%s.txt\"" % (info.DATA_TRANSACTIONS, i))

        # Raising error if one or more of the payment modes names provided are not existant.
        if len(valid_transactions_id) != len(transactions_id):
            raise Exception("0xetrn0011")

    def edit_transaction(self,
                        transaction_id: str,
                        amount: Union[int, float] = None,
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
            if i.get("transaction_id") == transaction_id:
                transaction: dict = i
                break
        else:
            raise Exception("0xetrn0006")

        # Updating the transaction, Verifying it and saving it to the transaction file.
        transaction.update(edit)
        self._verify_transaction(transaction, exists = True)
        self._write_transaction(transaction)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    def _verify_transaction_file_name(self, file_name: str) -> bool:

        # Verifying the file name
        return True if \
        file_name.__len__() == 21 and \
        file_name[:7] == "trn_id_" and \
        file_name[7:17].isdigit() and \
        file_name[17:] == ".txt" \
        else False

    def er_0xetrn0001(self) -> bool:

        # Capturing the names of the files present in the transactions data folder.
        try:
            transaction_files: list[str] = Indexer(info.DATA_TRANSACTIONS).get_files()
        except Exception:
            raise Exception("0xetrn0004")
        
        valid_files: list[str] = [i for i in transaction_files if self._verify_transaction_file_name(i)]
        invalid_files: list[str] = [i for i in transaction_files if i not in valid_files]

        if invalid_files.__len__() == 0:
            return True
        
        # To be continued...
        
    def er_0xetrn0002(self):
        self.er_0xetrn0001()

    def er_0xetrn0003(self):
        ...

    def er_0xetrn0004(self):
        ...

    def er_0xetrn0006(self) -> bool:
        if os.path.exists(info.DATA_TRANSACTIONS):
            return True
        else:
            if not os.path.exists(info.DATA_PATH):
                raise Exception("0xegbl0002")
            
        # Creating the transactions data folder.
        try:
            os.mkdir(info.DATA_TRANSACTIONS)
        except Exception:
            os.system("mkrdir \"%s\"" % info.DATA_TRANSACTIONS)

        if os.path.exists(info.DATA_TRANSACTIONS):
            return True
        else:
            return False