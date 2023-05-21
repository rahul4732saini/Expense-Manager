r"""
Module related to functions for sorting transactions.

This exports:

(Class) Sort:
-------------
-   datetime_added: return a list of transactions sorted on the basis of the datetime of creation.
-   amount: return a list of transactions sorted on the basis of amount.
-   transaction_datetime: return a list of transactions sorted on the basis of the datetime of transaction.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
except Exception:
    raise Exception("0xegbl0001")

class Sort:

    # Function to verify the arguments provided to the sort functions.
    def _verify_args(function):
        def wrapper(self, ascending: bool = True):
            if ascending.__class__ != bool:
                raise Exception("0xetrn01sr")

            return function(self, ascending)

        return wrapper            

    # General function for sorting transactions.
    def _sort(self,
              key,
              ascending: bool = True) -> list[dict]:
        return sorted(Manage().get_transactions(), key = key, reverse = not ascending)
    
    @_verify_args
    def datetime_added(self, ascending: bool = True) -> list[dict]:
        return self._sort(key = lambda trn: trn["datetime_added"], ascending = ascending)

    @_verify_args
    def amount(self, ascending: bool = True) -> list[dict]:
        return self._sort(key = lambda trn: trn["amount"], ascending = ascending)
    
    @_verify_args
    def transaction_datetime(self, ascending: bool = True) -> list[dict]:
        return self._sort(list, key = lambda trn: trn["transaction_datetime"], ascending = ascending)