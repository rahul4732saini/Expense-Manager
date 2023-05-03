from sys import path
path.append("..\\Expense Manager")

import os
import random
from typing import Union
from threading import Thread
from time import strftime, strptime

try:
    import data.info as info
    from common.directory import indexer
    from catagory import income, expense
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class manage:
    def _check_save_path(self) -> None:
        if os.path.exists(info.DATA_TRANSACTIONS) == False:
            raise Exception("0xetrn0004")

    def get_transactions(self) -> list:
        self._check_save_path()

        try:
            transaction_files:list = indexer(info.DATA_TRANSACTIONS).get_files()
        except Exception:
            raise Exception("0xetrn0010")

        i:str
        for i in transaction_files:
            if i.__len__() != 21:
                raise Exception("0xetrn0001")
            if i[-4:] != ".txt":
                raise Exception("0xetrn0002")
            if i[:7] != "trn_id_" or i[7:i.rfind(".")].isdigit() == False:
                raise Exception("0xetrn0001")

        return transaction_files

    def get_transactions_id(self) -> list:
        return [i[7:i.rfind(".")] for i in self.get_transactions()]

    def _create_transaction_id(self) -> None:
        transaction_id:str = str(random.randrange(1,10**10))
        
        while transaction_id in self.get_transactions_id():
            transaction_id = str(random.randrange(1,10**10))

        transaction_id = "%s%s" % ("0"*(10-transaction_id.__len__()),transaction_id) if transaction_id.__len__() < 10 else transaction_id
        self.transaction_id = transaction_id

    def _check_transaction_validity(self, transaction:dict, exists:bool) -> None:
        trn:dict = transaction

        try:
            if all(
                [
                trn.get("transaction_id") in self.get_transactions_id() if exists
                else trn.get("transaction_id").__class__ == str and trn.get("transaction_id").__len__() == 10 and trn.get("transaction_id").isdigit(),
                bool(strptime(trn.get("date_added"), "%d-%m-%Y")) and int(trn.get("date_added")[-4:]) <= int(strftime("%Y")),
                bool(strptime(trn.get("time_added"), "%H:%M")),
                trn.get("status") in pre_requisites.STATUS,
                trn.get("amount").__class__ in [int, float] and trn.get("amount") > 0,
                trn.get("transaction_type") in pre_requisites.TRANSACTION_TYPES,
                trn.get("transaction_mode").__class__ == str,
                trn.get("catagory").__class__ in [str, dict],
                trn.get("transaction_time") ==None or bool(strptime(trn.get("transaction_time"), "%H:%M")),
                trn.get("transaction_date") == None or bool(strptime(trn.get("transaction_date"), "%d-%m-%Y"))
                and int(trn.get("transaction_date")[-4:]) in range(1980, 2100),
                trn.get("description") == None or trn.get("description").__class__ == str and trn.get("description").__len__() <= 100
                ]
            ) == False:
                raise Exception
        except Exception:
            raise Exception("0xetrn0009") if exists == False else Exception("0xetrn0008")

        catagory:Union[str,dict] = trn.get("catagory")
        income_cat:bool = trn.get("transaction_type") == "income"

        if income_cat and catagory.__class__ == dict and catagory.get("others") == None or income_cat and catagory not in income().get_catagories():
            raise Exception("0xetrn0011")
        elif income_cat == False and catagory.__class__ == dict and catagory.get("others") == None or income_cat == False and catagory not in expense().get_catagories():
            raise Exception("0xetrn0011")

    def read_transactions(self) -> list:
        transaction_files:list = self.get_transactions()
        transactions:list = list()

        try:
            for i in transaction_files:
                with open("%s\\%s" % (info.DATA_TRANSACTIONS,i)) as file:
                    content:dict = eval(file.read().replace("\n",""))
                    self._check_transaction_validity(content, exists = True)
                    transactions.append(content)
        except Exception:
            raise Exception("0xetrn0003")

        return transactions

    def _write_transaction(self, transaction_dict:dict, exists:bool):
        transaction_id:str = transaction_dict.get("transaction_id")
        transaction:str = str(transaction_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")
        
        with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, transaction_id),'w') as file:
            file.write(transaction)

    def add_transaction(self,
                        amount:float,
                        transaction_type:str,
                        transaction_mode:str,
                        catagory:Union[str, dict],
                        time:str = None,
                        date:str = None,
                        description:str = None) -> None:
        
        thread = Thread(self._create_transaction_id(), daemon = True)
        thread.start()

        try:
            entry:dict = {
                "transaction_id": self.transaction_id,
                "date_added": strftime("%d-%m-%Y"),
                "time_added": strftime("%H:%M"),
                "status": "cleared",
                "amount": amount,
                "transaction_type": transaction_type,
                "transaction_mode": transaction_mode,
                "catagory": catagory,
                "transaction_time": time,
                "transaction_date": date,
                "description": description
            }
        except Exception:
            raise Exception("0xetrn0007")

        self._check_save_path()
        self._check_transaction_validity(entry, exists = False)
        self._write_transaction(entry, exists = False)

    def switch_transaction(self, transaction_id:str) -> None:
        if transaction_id not in self.get_transactions_id():
            raise Exception("0xetrn0005")

        try:
            with open("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS,transaction_id)) as file:
                transaction:dict = eval(file.read().replace("\n",""))
            
            if transaction not in self.read_transactions():
                raise Exception
            if transaction.get("status") not in ["cleared", "cancelled"]:
                raise Exception
        except Exception:
            raise Exception("0xetrn0006")

        trn_status:str = transaction.get("status")
        trn_status = "cleared" if trn_status == "cancelled" else "cancelled"

        transaction.update({"status": trn_status})
        self._write_transaction(transaction, exists = True)

    def delete_transaction(self, transactions_id:list) -> None:
        if transactions_id.__class__ not in [list, tuple, set]:
            raise Exception("0xetrn0012")
        
        i:str
        for i in transactions_id:
            try:
                os.remove("%s\\trn_id_%s.txt" % (info.DATA_TRANSACTIONS, i))
            except Exception:
                os.system("del \"%s\\trn_id_%s.txt\"" % (info.DATA_TRANSACTIONS, i))

    def edit_transaction(self,
                        transaction_id:str,
                        amount:float = None,
                        transaction_type:str = None,
                        transaction_mode:str = None,
                        catagory = None,
                        transaction_time:str = None,
                        transaction_date:str = None,
                        description:str = None) -> None:

        edit:dict = {key: value for key, value in locals().items() if value != None and key != "self" and key != "transaction_id"}

        try:
            i:dict
            for i in self.read_transactions():
                if i.get("transaction_id") == transaction_id:
                    content = i
                    break
        except Exception:
            raise Exception("0xetrn0006")

        content.update(edit)
        self._check_transaction_validity(content, exists = True)
        self._write_transaction(content, exists = True)