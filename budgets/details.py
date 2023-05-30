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

    import re
    import random
    import os.path
    import datetime
    import data.info as info
    from threading import Thread
    from common.directory import Indexer
    from transactions.catagory import Expense
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_budgets_id(self) -> list[str]:

        # Capturing budget files from the budgets data folder.
        try:
            budget_files: list[str] = Indexer(info.DATA_BUDGETS).get_files()
        except Exception:
            raise Exception("0xebgt0001")
        
        # Verifying the names of the budget files.
        i:str
        for i in budget_files:
            if not re.match("^bgt_id_[0-9]{10}.txt$", i):
                raise Exception("0xebgt0002")

        # Returning only the ID of the budgets as strings.
        return [i[7:-4] for i in budget_files]
    
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
                (   
                    # Verifying budget_ID
                    bgt["budget_id"] in self.get_budgets_id() if exists else re.match("^[0-9]{10}$", bgt["budget_id"]),

                    # Verifying datetime_added
                    bgt["datetime_added"].__class__ == datetime.datetime and bgt["datetime_added"].year <= datetime.datetime.today().year,

                    # Verifying range
                    bgt["range"].__class__ in (int, float) and bgt["range"] > 0,

                    # Verifying month & year
                    bgt["month"] in range(1, 13) and bgt["year"] in range(1980, 2100),

                    # Verifying catagories
                    bgt["catagories"] == None or (bgt["catagories"].__class__ == dict and 
                    all((key in Expense().get_catagories().keys() and value.__class__ in [int, float] for key, value in bgt["catagories"].items())) and
                    sum(bgt["catagories"].values()) <= bgt["range"]),
                )
            ):
                raise Exception
        except Exception:
            raise Exception("0xebgt0003")

    def get_budgets(self) -> list[dict]:

        # Caputring the budgets_id to retrive the contents of the associated budget files.
        budgets_id: list[str] = self.get_budgets_id()
        budgets: list[dict] = list()

        # Accessing the budget files, capturing the budgets and verifying them.
        i: str
        for i in budgets_id:
            with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, i), 'r') as file:
                try:
                    budget: dict = eval(file.read())
                    self._verify_budget(budget, exists = True)

                    # Checking for invalid budget_ID(s).
                    if budget["budget_id"] != i:
                        raise Exception
                except Exception:
                    raise Exception("0xebgt0004")

                # Checking for budgets with similar active month.
                if any(([budget["month"], budget["year"]] == [i["month"], i["year"]] for i in budgets)):
                    raise Exception("0xebgt0010")
                    
                budgets.append(budget)
        
        return budgets

    def _write_budget(self, budget: dict) -> None:
        
        # Converting the budget dictionary into a readable string format to be written in the file.
        with open("%s\\bgt_id_%s.txt" % (info.DATA_BUDGETS, budget["budget_id"]), 'w') as file:
            file.write(str(budget).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}"))

    def add_budget(self,
                   range: int | float,
                   month: int,
                   year: int,
                   catagories: dict = None) -> None:
        
        # Creating an unique budget ID
        thread = Thread(self._create_budget_id(), daemon = True)
        thread.start()

        if not hasattr(self, "_budget_id"):
            raise Exception("0xebgt0005")

        # Raising an error if a budget for the provided month already exists.
        if any((i["month"] == month and i["year"] == year for i in self.get_budgets())):
            raise Exception("0xebgt0009")

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

    def delete_budgets(self, budgets_id: str | list[str]) -> None:
        if budgets_id.__class__ not in [str, list]:
            raise Exception("0xebgt0009")
        
        budgets_id: set = set(budgets_id) if budgets_id.__class__ == list else {budgets_id}
        
        # List of budgets_id queued for deletion that exist, i.e., are valid.
        valid_budgets_id: set = {i for i in budgets_id if i in self.get_budgets_id()}

        # Deleting budget files with related budget_id.
        i: str
        for i in valid_budgets_id:
            os.system("del \"%s\\bgt_id_%s.txt\"" % (info.DATA_BUDGETS, i))

        # Raising error if one or more of the payment modes names provided are not existant.
        if len(valid_budgets_id) != len(budgets_id):
            raise Exception("0xebgt0007")

    def edit_budget(self,
                    budget_id: str,
                    range: int | float = None,
                    month: str = None,
                    year: str = None,
                    catagories: dict = None):

        # Dictionary of the edits to be updated in the budget.
        edit = {key:value for key, value in locals().items() if key not in ("self", "budget_id") and value != None}

        if edit.__len__() == 0:
            raise Exception("0xebgt0008")

        budgets: list[dict] = self.get_budgets()

        # Iterates through the budgets and checks if a budget exists with the provided budget ID.
        # Raises an error if no corresponding budget is found.
        i: dict
        for i in budgets:
            if i.get("budget_id") == budget_id:
                budget = i
                break
        else:
            raise Exception("0xebgt0006")
        
        # Updating the budget, Verifying it and saving it to the budget file.
        if "catagories" in edit.keys():
            budget["catagories"] = None

        budget.update(edit)

        # Raising an error if month or year is provided as an argument and a budget for the provided month already exists.
        if any((i in edit.keys() for i in ["month", "year"])) and any(([budget["month"], budget["year"]] == [i["month"], i["year"]] for i in budgets)):
            raise Exception("0xebgt0009")

        # Verifying the edited budget and saving it to the data folder.
        self._verify_budget(budget, exists = True)
        self._write_budget(budget)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...