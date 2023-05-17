from sys import path
path.append("..\\Expense Manager")

from details import Manage

class Sort:

    # General function for sorting transactions.
    def _sort(self, key, ascending = True, list = Manage().get_transactions()) -> list:
        return sorted(list, key = key, reverse = not ascending)

    def date_added(self, ascending: bool = True):
        return self._sort(key = lambda trn: trn["date_added"], ascending = ascending)

    def time_added(self, ascending: bool = True):
        return self._sort(key = lambda trn: trn["time_added"], ascending = ascending)

    def amount(self, ascending: bool = True):
        return self._sort(key = lambda trn: trn["amount"], ascending = ascending)

    # Upcoming function related to datetime are divided into priors and subsequent to keep
    # transactions with datetime provided aside from transactions with no datetime provided.

    def transaction_date(self, ascending: bool = True):
        prior = self._sort(
            list = [i for i in Manage().get_transactions() if i["transaction_datetime"] != None],
            key = lambda trn: trn["transaction_datetime"].date(),
            ascending = ascending
        )
        
        subsequent = [i for i in Manage().get_transactions() if i not in prior]
        
        return prior + subsequent

    def transaction_time(self, ascending: bool = True):
        prior = self._sort(
            list = [i for i in Manage().get_transactions() if i["transaction_datetime"] != None],
            key = lambda trn: trn["transaction_datetime"].time(),
            ascending = ascending
        )
        
        subsequent = [i for i in Manage().get_transactions() if i not in prior]
        
        return prior + subsequent
    
    def transaction_datetime(self, ascending: bool = True):
        prior = self._sort(
            list = [i for i in Manage().get_transactions() if i["transaction_datetime"] != None],
            key = lambda trn: trn["transaction_datetime"],
            ascending = ascending
        )
        
        subsequent = [i for i in Manage().get_transactions() if i not in prior]
        
        return prior + subsequent