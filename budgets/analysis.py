r"""
Module related to functions for the
analysis of budgets.

(Class) BudgetsNumber:
----------------------
-   total: returns the total number of budgets created.
-   successful: return the total number of successful budgets.
-   failed: returns the total number of failed budgets.
-   upcoming: returns the total number of budgets created for upcoming months.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
except:
    raise Exception("0xegbl0001")

class BudgetsNumber:
    def total(self) -> int:
        return Manage().get_budgets().__len__()

    def successful(self) -> int:
        return [i for i in Manage().get_budgets() if i["status"] == "success"]

    def failed(self) -> int:
        return [i for i in Manage().get_budgets() if i["status"] == "failed"]

    def upcoming(self) -> int:
        return [i for i in Manage().get_budgets() if i["status"] == "upcoming"]