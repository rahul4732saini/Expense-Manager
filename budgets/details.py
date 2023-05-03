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
    from transactions.catagory import expense
except Exception:
    raise Exception("0xegbl0001")

class manage:
    def _check_save_path(self) -> None:
        if os.path.exists(info.DATA_BUDGETS) == False:
            raise Exception("0xebud0001")

    def get_budgets(self) -> list:
        self._check_save_path()
        
        try:
            budget_files:list = indexer(info.DATA_BUDGETS).get_files()
        except Exception:
            raise Exception("0xebgt0001")
        
        i:str
        for i in budget_files:
            if i.__len__() != 21:
                raise Exception("0xebgt0002")
            if i[-4:] != ".txt":
                raise Exception("0xebgt0003")
            if i[:7] != "bgt_id_" or i[7:i.rfind(".")].isdigit() == False:
                raise Exception("0xetbgt0002")
            
        return budget_files
    
    def get_budgets_id(self) -> list:
        return [i[7:i.rfind(".")] for i in self.get_budgets()]
    
    def _create_budget_id(self) -> None:
        budget_id:int = str(random.randrange(10**10))

        while budget_id in self.get_budgets_id():
            budget_id = str(random.randrange(10**10))

        budget_id:str = "%s%s" % ("0"*(10-budget_id.__len__()), budget_id) if budget_id.__len__() < 10 else budget_id
        self.budget_id = budget_id

    def _check_budget_validity(self, budget:dict, exists:bool) -> None:
        bgt:dict = budget

        try:
            if all(
                [
                    bgt.get("budget_id") in self.get_budgets_id() if exists
                    else bgt.get("budget_id").__class__ == str and bgt.get("budget_id").isdigit() and bgt.get("budget_id").__len__() == 10,
                    bool(strptime(bgt.get("date_added"), "%d-%m-%Y")) and int(bgt.get("date_added")[-4:]) <= int(strftime("%Y")),
                    bool(strptime(bgt.get("time_added"), "%H:%M")),
                    bgt.get("range").__class__ in [int, float] and bgt.get("range") > 0,
                    bool(strptime("%s-%s" % (bgt.get("month"), bgt.get("year")), "%m-%Y")),
                    int(bgt.get("year")) in range(1980, 2100),
                    bgt.get("catagories").__class__ == dict,
                    [i in expense().get_catagories().keys() for i in bgt.get("catagories").keys()]
                ]
            ) == False:
                raise Exception
        except Exception:
            raise Exception("0xebgt0004") if exists == False else Exception("0xebgt0005")

    def read_budgets(self) -> list:
        budget_files:list = self.get_budgets()
        budgets:list = list()

        try:
            for i in budget_files:
                with open("%s\\%s" % (info.DATA_BUDGETS, i)) as file:
                    content:dict = eval(file.read().replace("\n", ""))
                    self._check_budget_validity(content, exists = True)
                    budgets.append(content)
        except Exception:
            raise Exception("0xebgt0006")
        
        return budgets
    
    def _write_budget(self, budget_dict:dict, exists:bool) -> None:
        budget_id:str = budget_dict.get("budget_id")
        budget:str = str(budget_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")
        
        with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, budget_id),'w') as file:
            file.write(budget)

    def add_budget(self,
                   range:Union[int, float],
                   month:str,
                   year:str,
                   catagories:dict) -> None:
        
        thread = Thread(self._create_budget_id(), daemon = True)
        thread.start()

        try:
            entry = {
                "budget_id": self.budget_id,
                "date_added": strftime("%d-%m-%Y"),
                "time_added": strftime("%H:%M"),
                "range": range,
                "month": month,
                "year": year,
                "catagories": catagories
            }
        except Exception:
            raise Exception("0xebgt0007")

        self._check_save_path()
        self._check_budget_validity(entry, exists = False)
        self._write_budget(entry, exists = False)

    def delete_budgets(self, budgets_id:Union[list, tuple, set]):
        if budgets_id.__class__ not in [list, tuple, set]:
            raise Exception("0xebgt0012")
        
        i:str
        for i in budgets_id:
            try:
                os.remove("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, i))
            except Exception:
                os.system("del \"%s\\bgt_id_%s.txt\"" % (info.DATA_BUDGETS, i))

    def edit_budget(self,
                    budget_id:str,
                    range:Union[int, float] = None,
                    month:str = None,
                    year:str = None,
                    catagories:dict = None):
        
        edit = {key:value for key, value in locals().items() if key != "self" and key != "budget_id" and value != None}

        try:
            i:dict
            for i in self.read_budgets():
                if i.get("budget_id") == budget_id:
                    content = i
                    break
        except Exception:
            raise Exception("0xebgt0009")
        
        content.update(edit)
        self._check_budget_validity(content, exists = True)
        self._write_budget(content, exists = True)