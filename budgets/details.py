try:
    from sys import path
    path.append("..\\Expense Manager")

    import os
    import random
    import datetime
    from typing import Union
    from threading import Thread
    from time import strftime, strptime
    import data.info as info
    from common.directory import Indexer
    from transactions.catagory import Expense
except Exception:
    raise Exception("0xegbl0001")

class manage:
    def get_budgets_id(self) -> list:        
        try:
            budget_files: list = Indexer(info.DATA_BUDGETS).get_files()
        except Exception:
            raise Exception("0xebgt0001")
        
        i:str
        for i in budget_files:
            if i.__len__() != 21 or i[:7] != "bgt_id_" or i[7:i.rfind(".")].isdigit() == False:
                raise Exception("0xebgt0002")
            if i.removesuffix(".txt") == i:
                raise Exception("0xebgt0003")
            
        return [i[7:i.rfind(".")] for i in budget_files]
    
    def _create_budget_id(self) -> None:
        budget_id: int = str(random.randrange(10**10))

        while budget_id in self.get_budgets_id():
            budget_id = str(random.randrange(10**10))

        budget_id: str = "%s%s" % ("0"*(10-budget_id.__len__()), budget_id) if budget_id.__len__() < 10 else budget_id
        self._budget_id = budget_id

    def _check_budget_validity(self, budget: dict, exists: bool) -> None:
        bgt: dict = budget

        try:
            if all(
                [   
                    # Verifying budget_ID
                    bgt.get("budget_id") in self.get_budgets_id() if exists
                    else bgt.get("budget_id").__class__ == str and bgt.get("budget_id").isdigit() and bgt.get("budget_id").__len__() == 10,

                    # Verifying datetime_added
                    bool(strptime(bgt.get("date_added"), "%d-%m-%Y")) and int(bgt.get("date_added")[-4:]) <= int(strftime("%Y")),
                    bool(strptime(bgt.get("time_added"), "%H:%M")),

                    # Verifying range
                    bgt.get("range").__class__ in [int, float] and bgt.get("range") > 0,

                    # Verifying month & year
                    bool(strptime("%s-%s" % (bgt.get("month"), bgt.get("year")), "%m-%Y")),
                    int(bgt.get("year")) in range(1980, 2100),

                    # Verifying catagories
                    bgt.get("catagories") == None or bgt.get("catagories").__class__ == dict and all([i in Expense().get_catagories().keys() for i in bgt.get("catagories").keys()])
                ]
            ) == False:
                raise Exception
        except Exception:
            raise Exception("0xebgt0004") if exists == False else Exception("0xebgt0005")

    def get_budgets(self) -> list:
        budgets_id: list = self.get_budgets_id()
        budgets: list = list()

        try:
            for i in budgets_id:
                with open("%s\\%s.txt" % (info.DATA_BUDGETS, i), 'r') as file:
                    content: dict = eval(file.read().replace("\n", ""))

                    self._check_budget_validity(content, exists = True)
                    budgets.append(content)
        except Exception:
            raise Exception("0xebgt0006")
        
        return budgets
    
    def _write_budget(self, budget_dict: dict) -> None:
        budget_id: str = budget_dict.get("budget_id")
        budget: str = str(budget_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")
        
        with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, budget_id), 'w') as file:
            file.write(budget)

    def add_budget(self,
                   range: Union[int, float],
                   month: int,
                   year: int,
                   catagories: dict = None) -> None:
        
        thread = Thread(self._create_budget_id(), daemon = True)
        thread.start()

        if not hasattr(self, "_budget_id"):
            raise Exception("0xebgt0007")

        entry = {
            "budget_id": self._budget_id,
            "datetime_added": datetime.datetime.today(),
            "range": range,
            "month": month,
            "year": year,
            "catagories": catagories
        }

        if os.path.exists(info.DATA_BUDGETS) == False:
            raise Exception("0xebgt0001")

        self._check_budget_validity(entry, exists = False)
        self._write_budget(entry)

    def delete_budgets(self, budgets_id: Union[str, list[str]]):
        if budgets_id.__class__ not in [str, list[str]]:
            raise Exception("0xebgt0012")
        
        i: str
        for i in budgets_id:
            try:
                os.remove("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, i))
            except Exception:
                os.system("del \"%s\\bgt_id_%s.txt\"" % (info.DATA_BUDGETS, i))

    def edit_budget(self,
                    budget_id: str,
                    range: Union[int, float] = None,
                    month: str = None,
                    year: str = None,
                    catagories: dict = None):
        
        if all([value == None for key, value in locals() if key not in ["self", "budget_ud"]]):
            raise Exception()

        edit = {key:value for key, value in locals().items() if key != "self" and key != "budget_id" and value != None}

        try:
            i: dict
            for i in self.get_budgets():
                if i.get("budget_id") == budget_id:
                    content = i
                    break
        except Exception:
            raise Exception("0xebgt0009")
        
        content.update(edit)
        self._check_budget_validity(content, exists = True)
        self._write_budget(content, exists = True)