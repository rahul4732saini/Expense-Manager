r"""
Module related to functions required for the
management and troubleshooting of budgets.

This Exports:

(Class) Manage:
---------------
-   get_budgets_id: return a list of budgets ID.
-   get_budgets: return a list of all existing valid budgets in the form of dictionaries.
-   add_budget: used to create a new budget.
-   delete_budget: used to delete the budgets corresponding to the budgets ID provided as str / list.
-   edit_budget: used to edit the details of the budget corresponding to the budget ID provided.
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
    from common.directory import Indexer
    from transactions.catagory import Expense
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_budgets_id(self) -> list:

        # Capturing budget files from the budgets data folder.
        try:
            budget_files: list = Indexer(info.DATA_BUDGETS).get_files()
        except Exception:
            raise Exception("0xebgt0001")
        
        # Verifying the names of the budget files.
        i:str
        for i in budget_files:
            if i.__len__() != 21 or i[:7] != "bgt_id_" or i[7:i.rfind(".")].isdigit() == False:
                raise Exception("0xebgt0002")
            if i.removesuffix(".txt") == i:
                raise Exception("0xebgt0003")
            
        # Returning only the ID of the budgets as strings.
        return [i[7:i.rfind(".")] for i in budget_files]
    
    def _create_budget_id(self) -> None:
        # The max length of the ID is 10 digits.
        budget_id: str = str(random.randrange(10**10))

        # While loop is called to define another ID if the ID generated already exists.
        while budget_id in self.get_budgets_id():
            budget_id = str(random.randrange(10**10))

        # Changes the length of the ID by adding 0s in the begining if the length is less than 10.
        budget_id: str = "%s%s" % ("0"*(10-budget_id.__len__()), budget_id) if budget_id.__len__() < 10 else budget_id
        self._budget_id = budget_id

    def _verify_budget(self, bgt: dict, exists: bool) -> None:
        # budget_dictionary as namespace bgt

        try:
            if not all(
                [   
                    # Verifying budget_ID
                    bgt.get("budget_id") in self.get_budgets_id() if exists
                    else bgt.get("budget_id").__class__ == str and bgt.get("budget_id").isdigit() and bgt.get("budget_id").__len__() == 10,

                    # Verifying datetime_added
                    bgt.get("datetime_added").__class__ == datetime.datetime and bgt.get("datetime_added").year <= datetime.datetime.today().year,

                    # Verifying range
                    bgt.get("range").__class__ in [int, float] and bgt.get("range") > 0,

                    # Verifying month & year
                    bgt.get("month") in range(1, 13) and bgt.get("year") in range(1980, 2100),

                    # Verifying catagories
                    bgt["catagories"] == None or (bgt["catagories"].__class__ == dict and 
                    all([i in Expense().get_catagories().keys() for i in bgt["catagories"].keys()]) and
                    all([i.__class__ in [int, float] for i in bgt["catagories"].values()]) and
                    sum(bgt["catagories"].values()) <= bgt["range"])
                ]
            ):
                raise Exception
        except Exception:
            raise Exception("0xebgt0004")

    def get_budgets(self) -> list:
        budgets_id: list[str] = self.get_budgets_id()
        budgets: list[dict] = list()

        # Accessing the budget files, capturing the budgets and verifying them.
        try:
            i: str
            for i in budgets_id:
                with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, i), 'r') as file:
                    content: dict = eval(file.read().replace("\n", ""))

                    self._verify_budget(content, exists = True)
                    budgets.append(content)
        except Exception:
            raise Exception("0xebgt0006")
        
        return budgets
    
    def _write_budget(self, budget_dict: dict) -> None:
        
        # Retrieving the budget ID to access the related budget file.
        budget_id: str = budget_dict.get("budget_id")

        # Converting the budget dictionary into a readable string format to be written in the file.
        budget: str = str(budget_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")
        
        with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, budget_id), 'w') as file:
            file.write(budget)

    def add_budget(self,
                   range: Union[int, float],
                   month: int,
                   year: int,
                   catagories: dict = None) -> None:
        
        # Creating an unique budget ID
        thread = Thread(self._create_budget_id(), daemon = True)
        thread.start()

        if not hasattr(self, "_budget_id"):
            raise Exception("0xebgt0007")

        if any([i["month"] == month and i["year"] == year for i in self.get_budgets()]):
            raise Exception("0xebgt0012")

        entry = {
            "budget_id": self._budget_id,
            "datetime_added": datetime.datetime.today(),
            "range": range,
            "month": month,
            "year": year,
            "catagories": catagories
        }

        # Verifying and saving the budget into a file.
        self._verify_budget(entry, exists = False)
        self._write_budget(entry)

    def delete_budgets(self, budgets_id: Union[str, list[str]]):
        if budgets_id.__class__ not in [str, list]:
            raise Exception("0xebgt0012")
        
        budgets_id = budgets_id if budgets_id.__class__ == list else [budgets_id]

        if len(budgets_id) > len(self.get_budgets_id()):
            raise Exception("0xebgt0008")
        
        # List of budgets_id queued for deletion that exist, i.e., are valid.
        valid_budgets_id = [i for i in budgets_id if i in self.get_budgets_id()]
        
        # Deleting budget files with related budget_id.
        i: str
        for i in budgets_id:
            try:
                os.remove("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, i))
            except Exception:
                os.system("del \"%s\\bgt_id_%s.txt\"" % (info.DATA_BUDGETS, i))

        # Raising error if one or more of the payment modes names provided are not existant.
        if len(valid_budgets_id) != len(budgets_id):
            raise Exception("0xebgt0010")

    def edit_budget(self,
                    budget_id: str,
                    range: Union[int, float] = None,
                    month: str = None,
                    year: str = None,
                    catagories: dict = None):

        # Dictionary of the edits to be updated in the budget.
        edit = {key:value for key, value in locals().items() if key not in ["self", "budget_id"] and value != None}

        if edit.__len__() == 0:
            raise Exception("0xebgt0011")

        # Iterates through the budgets and checks if a budget exists with the provided budget ID.
        # Raises an error if no corresponding budget is found.
        i: dict
        for i in self.get_budgets():
            if i.get("budget_id") == budget_id:
                content = i
                break
        else:
            raise Exception("0xebgt0009")
        
        # Updating the budget, Verifying it and saving it to the budget file.
        content.update(edit)
        self._verify_budget(content, exists = True)
        self._write_budget(content)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...