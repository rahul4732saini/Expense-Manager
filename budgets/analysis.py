r"""
Module related to functions used
for the analysis of budgets.

This exports:

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
        return list(filter(lambda bgt: bgt["status"] == "success"), Manage().get_budgets())

    def failed(self) -> int:
        return list(filter(lambda bgt: bgt["status"] == "failed"), Manage().get_budgets())

    def upcoming(self) -> int:
        return list(filter(lambda bgt: bgt["status"] == "upcoming"), Manage().get_budgets())
    
# pending...