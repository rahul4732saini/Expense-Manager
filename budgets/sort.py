r"""
Module related to functions for sorting budgets.

This exports:

(Class) Sort:
-------------
-   datetime_added: return a list of budgets sorted on the basis of the datetime of creation.
-   range: return a list of budgets sorted on the basis of range.
-   active_month: return a list of budgets sorted on the basis of the active month of the budgets.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
    from datetime import date
except Exception:
    raise Exception("0xegbl0001")

class Sort:

    # Function to verify the arguments provided to the sort functions.
    def _verify_args(function):
        def wrapper(self, ascending: bool = True):
            if ascending.__class__ != bool:
                raise Exception("0xebgt01sr")
            
            return function(self, ascending = ascending)

        return wrapper

    # General function for sorting transactions.
    def _sort(self,
              key,
              list = Manage().get_budgets(),
              ascending = True) -> list[dict]:
        return sorted(list, key = key, reverse = not ascending)
    
    @_verify_args
    def datetime_added(self, ascending = True) -> list[dict]:
        return self._sort(key = lambda bgt: bgt["datetime_added"], ascending = ascending)
    
    @_verify_args
    def range(self, ascending = True):
        return self._sort(key = lambda bgt: bgt["range"], ascending = ascending)
    
    @_verify_args
    def active_month(self, ascending = True):
        return self._sort(key = lambda bgt: date(bgt["year"], bgt["month"], 15), ascending = ascending)