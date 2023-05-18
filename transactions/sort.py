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
                raise Exception("0xesrt0001")

            return function(self, ascending)

        return wrapper            

    # General function for sorting transactions.
    def _sort(self,
              key,
              list: list[dict] = Manage().get_transactions(),
              ascending: bool = True) -> list[dict]:
        return sorted(list, key = key, reverse = not ascending)
    
    @_verify_args
    def datetime_added(self, ascending: bool = True) -> list[dict]:
        return self._sort(key = lambda trn: trn["datetime_added"], ascending = ascending)

    @_verify_args
    def amount(self, ascending: bool = True) -> list[dict]:
        return self._sort(key = lambda trn: trn["amount"], ascending = ascending)

    # Upcoming function related to datetime is divided into priors and subsequent to keep
    # transactions with datetime provided aside from transactions with no datetime provided.
    
    @_verify_args
    def transaction_datetime(self, ascending: bool = True) -> list[dict]:
        prior: list[dict] = self._sort(
            list = [i for i in Manage().get_transactions() if i["transaction_datetime"] != None],
            key = lambda trn: trn["transaction_datetime"],
            ascending = ascending
        )
        
        subsequent: list[dict] = [i for i in Manage().get_transactions() if i not in prior]
        return prior + subsequent
    
print(Sort().datetime_added())