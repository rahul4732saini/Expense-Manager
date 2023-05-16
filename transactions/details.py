r"""
Module related to functions required for the
management and troubleshooting of transacvtions.

This exports:

(Class) Manage:
    get_transactions_id: returns the ID of the transactions as strings.
    get_transactions: return a list of all existing valid transactions dictionaries.
    add_transaction: used to create a new transaction.
    switch_transaction: used to switch transaction status between upcoming - cleared - cancelled.
    delete_transaction: used to delete the transactions corresponding to the transactions ID provided as str or list
    edit_transaction: used to edit the details of the transaction corresponding to the transaction ID provided.
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
    from common.directory import indexer
    from catagory import income, expense
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class manage:
    def get_transactions_id(self) -> list[str]:

        # Capturing transaction files from the transactions data folder.
        try:
            transaction_files: list[str] = indexer(info.DATA_TRANSACTIONS).get_files()
        except Exception:
            raise Exception("0xetrn0004")

        # Verifying the names of the transaction files.
        i: str
        for i in transaction_files:
            if i.__len__() != 21 or i[:7] != "trn_id_" or i[7:i.rfind(".")].isdigit() == False:
                raise Exception("0xetrn0001")
            if i.removesuffix(".txt") == i:
                raise Exception("0xetrn0002")

        # Returning only the ID of the files/transactions as strings.
        return [i[7:i.rfind(".")] for i in transaction_files]

    def _create_transaction_id(self) -> None:
        # The max length of the ID is 10 digits.
        transaction_id: str = str(random.randrange(1,10**10))
        
        # While loop is called to define another ID if the ID generated already exists.
        while transaction_id in self.get_transactions_id():
            transaction_id: str = str(random.randrange(1,10**10))

        # Changes the length of the ID by adding 0s if the length is less than 10.
        transaction_id = "%s%s" % ("0"*(10-transaction_id.__len__()),transaction_id) if transaction_id.__len__() < 10 else transaction_id
        self._transaction_id: str = transaction_id

    def _verify_transaction(self, trn: dict, exists: bool) -> None:
        # transaction_dictionary as namespace trn

        if all(
            [
                # Verifying transaction_ID
                trn.get("transaction_id") in self.get_transactions_id() if exists
                else trn.get("transaction_id").__class__ == str and trn.get("transaction_id").__len__() == 10 and trn.get("transaction_id").isdigit(),

                # Verifying date_added
                trn.get("date_added").__class__ == datetime.date and trn.get("date_added").year in range(1980, datetime.datetime.now().year+1),
                trn.get("time_added").__class__ == datetime.time,

                trn.get("status") in pre_requisites.STATUS, # Verifying status
                trn.get("amount").__class__ in [int, float] and trn.get("amount") > 0, # Verifying amount
                trn.get("transaction_type") in pre_requisites.TRANSACTION_TYPES, # Verifying transaction_type
                trn.get("payment_mode") in pay_mode.Manage().get_mode_names(), # Verifying payment_mode
                trn.get("catagory").__class__ in [str, dict], # Verifying catagory

                # Verifying transaction_time & transaction_time
                trn.get("transaction_time").__class__ in [None, datetime.time],
                trn.get("transaction_date") == None or trn.get("transaction_date").__class__ == datetime.date and trn.get("transaction_date").year in range(1980, 2100),

                # Verifying description
                trn.get("description") == None or trn.get("description").__class__ == str and trn.get("description").__len__() <= 100
            ]
        ) == False:
            raise Exception("0xetrn0008")

        catagory: Union[str,dict] = trn.get("catagory")
        income_catagory: bool = trn.get("transaction_type") == "income"

        if any(
            [   
                # Verifying catagory if transaction type == "income"
                income_catagory and (catagory.__class__ == dict and catagory.get("others") == None or
                catagory.__class__ == str and catagory not in income().get_catagories()),

                # Verifying catagory if transaction_type == "expense"
                income_catagory == False and (catagory.__class__ == dict and catagory.get("others") == None or
                catagory.__class__ == str and catagory not in expense().get_catagories()),
            ]
        ):
            raise Exception("0xetrn0011")

    def get_transactions(self) -> list[dict]:
        transaction_files: list[str] = self.get_transactions_id()
        transactions: list[dict] = list()

        # Reading the transactions files, capturing the transactions and verifying them.
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

    def _write_transaction(self, transaction_dict: dict):

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
                        time: datetime.time = None,
                        date: datetime.date = None,
                        description: str = None) -> None:
        
        # Creating a unique transaction ID
        thread = Thread(self._create_transaction_id(), daemon = True)
        thread.start()

        if hasattr(self, "_transaction_id") == False:
            raise Exception("0xetrn0007")
        
        entry: dict = {
            "transaction_id": self._transaction_id,
            "time_added": datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute),
            "date_added": datetime.date.today(),
            "status": "cleared",
            "amount": amount,
            "transaction_type": transaction_type,
            "payment_mode": payment_mode,
            "catagory": catagory,
            "transaction_time": time,
            "transaction_date": date,
            "description": description
        }

        if os.path.exists(info.DATA_TRANSACTIONS) == False:
            raise Exception("0xetrn0004")

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
            
            if transaction not in self.get_transactions() or transaction.get("status") not in pre_requisites.STATUS:
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
            raise Exception("0xetrn0012")

        transactions_id = transactions_id if transactions_id.__class__ == list else [transactions_id]

        if transactions_id.__len__() > self.get_transactions_id().__len__():
            raise Exception("0xetrn0012")

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
        if valid_transactions_id.__len__() != transactions_id.__len__():
            raise Exception("0xetrn0013")

    def edit_transaction(self,
                        transaction_id: str,
                        amount: Union[int, float] = None,
                        transaction_type: str = None,
                        payment_mode: str = None,
                        catagory = None,
                        transaction_time: datetime.time = None,
                        transaction_date: datetime.date = None,
                        description: str = None) -> None:

        # Dictionary of the edits to be updated in the transaction.
        edit: dict = {key: value for key, value in locals().items() if value != None and key not in ["self", "transaction_id"]}

        if edit.__len__() == 0:
            raise Exception("0xetrn0014")

        # Iterates through the transactions and checks if a transaction exists with the provided transaction ID.
        # raises an error if no corresponding transaction is found.
        try:
            i: dict
            for i in self.get_transactions():
                if i.get("transaction_id") == transaction_id:
                    transaction: dict = i
                    break
            else:
                raise Exception
        except Exception:
            raise Exception("0xetrn0006")

        # Updating the transaction, Verifying it and saving it to the transaction file. 
        transaction.update(edit)
        self._verify_transaction(transaction, exists = True)
        self._write_transaction(transaction)

class TroubleShoot:
    ...