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

    from datetime import date
    from details import Manage
except Exception:
    raise Exception("0xegbl0001")

class Sort:

    # Function to verify the arguments provided to the sort functions.
    def _verify_args(function):
        def wrapper(self, ascending: bool = True):
            assert ascending.__class__ == bool, '0xdbgt01sr'
            
            return function(self, ascending = ascending)

        return wrapper

    # General function for sorting transactions.
    def _sort(self,
              key,
              ascending = True) -> list[dict]:
        return sorted(Manage().get_budgets(), key = key, reverse = not ascending)
    
    @_verify_args
    def datetime_added(self, ascending = True) -> list[dict]:
        return self._sort(key = lambda bgt: bgt["datetime_added"], ascending = ascending)
    
    @_verify_args
    def range(self, ascending = True) -> list[dict]:
        return self._sort(key = lambda bgt: bgt["range"], ascending = ascending)
    
    @_verify_args
    def active_month(self, ascending = True) -> list[dict]:
        return self._sort(key = lambda bgt: date(bgt["year"], bgt["month"], 1), ascending = ascending)