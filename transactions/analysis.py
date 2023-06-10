r"""
Module related to functions used
for the analysis of transactions.

This exports:

(Class) TransactionNumber:
--------------------------
-   lifetime: returns the total number of transactions ever added.
-   year: returns the total number of transactions added in the provided year.
-   month: returns the total number of transactions added in the provided month and year.
-   day: returns the total number of transactions added on the provided date.

(Class) StatusIncome:
---------------------
-   lifetime: returns the total sum of money ever gained.
-   year: returns the total sum of money gained in the provided year.
-   month: return the total sum of money gained in the provided month and year.
-   day: return the total sum of money gained on the provided date.

(Class) StatusExpense:
----------------------
-   lifetime: return the total sum of money ever spent.
-   year: returns the total sum of money spent in the provided year.
-   month: return the total sum of money spent in the provided month and year.
-   day: return the total sum of money spent on the provided date.

(Class) Balance:
----------------
-   lifetime: returns the overall balance of the transactions.
-   year: returns the balance of the transactions added in the provided year
-   month: returns the balance of the transactions added in the provided month and year
-   day: returns the balance of the transactions added on the provided date.

(Class) AverageTransactionIncome:
---------------------------------
-   lifetime: returns the average amount of money ever gained.
-   year: returns the average amount of money gained in the provided year.
-   month: returns the average amount of money gained in the provided month and year.
-   day: returns the average amount of money gained on the provided date.

(Class) AverageTransactionExpense:
----------------------------------
-   lifetime: returns the average amount of money ever spent.
-   year: returns the average amount of money spent in the provided year.
-   month: returns the average amount of money spent in the provided month and year.
-   day: returns the average amount of money spent on the provided date.

(Class) CatagoryDistribution:
-----------------------------
-   lifetime: reuturns a dictionary of the catagory distribution of all the transactions.
-   year: returns a dictionary of the catagory distribtuion of the transactions in the provided year.
-   month: returns a dictionary of the catagory distribtuion of the transactions in the provided month and year.
-   day: returns a dictionary of the catagory distribtuion of the transactions on the provided date.

(Class) PaymentModeDistribution:
--------------------------------
-   lifetime: reuturns a dictionary of the payment mode distribution of all the transactions.
-   year: returns a dictionary of the payment mode distribtuion of the transactions in the provided year.
-   month: returns a dictionary of the payment mode distribtuion of the transactions in the provided month and year.
-   day: returns a dictionary of the payment mode distribtuion of the transactions on the provided date.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from datetime import date
    from functools import wraps
    from abc import ABC, abstractmethod
    from transactions.details import Manage
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

# Base class for all following analytic classes.
class Status(ABC):

    @abstractmethod
    def lifetime(self):
        ...

    @abstractmethod
    def year(self):
        ...

    @abstractmethod
    def month(self):
        ...

    @abstractmethod
    def day(self):
        ...
    
    # The below function is restricted to keyword arguments only!
    def _verify_arguments(*,
                          year: int,
                          month: int = None,
                          day: int = None):

        def suffix(function):

            @wraps(function)
            def wrapper(self, *,
                        year: int = year,
                        month: int = month,
                        day: int = day) -> None:
                
                # Dictionary of all the keywords arguments to be provided to the function.
                kwargs = {key: value for key, value in locals().items() if value != None and key not in ("self", "function")}

                # Verifying arguments.
                try:
                    if year not in range(1980, 2100) or month != None and month not in range(1, 13):
                        raise Exception
                    
                    if day != None:
                        date(year, month, day)

                    return function(self, **kwargs)
                except Exception:
                    raise Exception("0xetrn01an")

            return wrapper
        
        return suffix
    
    def _evaluate_keys(self, transactions: list[dict], key: str) -> dict:

        # Validating the transaction keys.
        assert key in pre_requisites.TRANSACTION_KEYS, "0xetrn01an"
        
        # key -> key; value -> number of occurance of the key.
        distribution:dict = dict()

        i: dict
        for i in transactions:
            if i[key] in distribution:
                distribution[i[key]] += 1
            else:
                distribution[i[key]] = 1

        return distribution

class TransactionNumber(Status):
    def lifetime(self) -> int:
        return len(Manage().get_transactions())
    
    @property
    def transactions(self) -> list[dict]:
        return Manage().get_transactions()

    @Status._verify_arguments   
    def year(self, year: int) -> int:
        return len([i for i in self.transactions if i["transaction_datetime"].year == year])

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int:
        return len([i for i in self.transactions if i["transaction_datetime"].year == year and i["transaction_datetime"].month == month])

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int:
        return len([i for i in self.transactions if i["transaction_datetime"].date() == date(year, month, day)])

class StatusIncome(Status):
    @property
    def transaction_type(self):
        return "income" if "Income" in self.__class__.__name__ else "expense"
    
    @property
    def transactions(self) -> list[dict]:
        return [i for i in Manage().get_transactions() if i["transaction_type"] == self.transaction_type]
    
    def lifetime(self) -> int | float:    
        return(sum([i["amount"] for i in self.transactions]))

    @Status._verify_arguments
    def year(self, year: int) -> int | float:
        return sum([i["amount"] for i in self.transactions if i["transaction_datetime"].year == year])
    
    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int | float:
        return sum([i["amount"] for i in self.transactions if i["transaction_datetime"].year == year and i["transaction_datetime"].month == month])
    
    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int | float:
        return sum([i["amount"] for i in self.transactions if i["transaction_datetime"].date() == date(year, month, day)])
    
class StatusExpense(StatusIncome, Status):
    def __init__(self):
        super().__init__()

    def lifetime(self) -> int | float:
        return super().lifetime()
    
    def year(self, year: int) -> int | float:
        return super().year(year = year)
    
    def month(self,
              month: int,
              year: int) -> int | float:
        return super().month(month = month, year = year)
    
    def day(self,
            day: int,
            month: int,
            year: int) -> int | float:
        return super().day(day = day, month = month, year = year)

class Balance(Status):
    def lifetime(self) -> int | float:
        return StatusIncome().lifetime() - StatusExpense().lifetime()
    
    def year(self, year: int) -> int | float:
        return StatusIncome().year(year = year) - StatusExpense().year(year = year)
    
    def month(self,
              month: int,
              year: int) -> int | float:
        return StatusIncome().month(month = month, year = year) - StatusExpense().month(month = month, year = year)
    
    def day(self,
            day: int,
            month: int,
            year: int) -> int | float:
        return StatusIncome().day(day = day, month = month, year = year) - StatusExpense().day(day = day, month = month, year = year)
    
class AverageTransactionIncome(Status):
    @property
    def transaction_type(self) -> str:
        return "income" if "Income" in self.__class__.__name__ else "expense"

    @property
    def transactions(self) -> list[dict]:
        return [i for i in Manage().get_transactions() if i["transaction_type"] == self.transaction_type]

    def lifetime(self) -> int | float:
        return sum([i["amount"] for i in self.transactions]) / len(self.transactions)

    @Status._verify_arguments
    def year(self, year: int) -> int | float:
        if target_transactions := [i for i in self.transactions if i["transaction_datetime"].year == year]:
            return sum([i["amount"] for i in target_transactions]) / len(target_transactions)
        
        return 0

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int | float:
         if target_transactions := [i for i in self.transactions if i["transaction_datetime"].month == month and i["transaction_datetime"].year == year]:
            return sum([i["amount"] for i in target_transactions]) / len(target_transactions)
         
         return 0
    
    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int | float:
        if target_transactions := [i for i in self.transactions if i["transaction_datetime"].date() == date(year, month, day)]:
            return sum([i["amount"] for i in target_transactions]) / len(target_transactions)
        
        return 0

class AverageTransactionExpense(AverageTransactionIncome, Status):
    def __init__(self):
        super().__init__()

    def lifetime(self) -> int | float:
        return super().lifetime()
    
    @Status._verify_arguments
    def year(self, year: int) -> int | float:
        return super().year(year = year)
    
    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int | float:
        return super().month(month = month, year = year)
    
    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int | float:
        return super().day(day = day, month = month, year = year)

class CatagoryDistribution(Status):
    def __init__(self, transaction_type):
        self.transaction_type = transaction_type

    def __setattr__(self, name: str, value: object):
        if name == "transaction_type" and value not in pre_requisites.TRANSACTION_TYPES:
            raise Exception()
        
        return super().__setattr__(name, value)

    @property
    def transactions(self) -> list[dict]:
        return [i for i in Manage().get_transactions() if i["transaction_type"] == self.transaction_type]

    def lifetime(self) -> dict:
        return super()._evaluate_keys(self.transactions, key = "catagory")

    @Status._verify_arguments
    def year(self, year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].year == year], key = "catagory")

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].month == month and i["transaction_datetime"].year == year], key = "catagory")

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].date() == date(year, month, day)], key = "catagory")

class PaymodeModeDistribution(Status):
    @property
    def transactions(self) -> list[dict]:
        return Manage().get_transactions()

    def lifetime(self) -> dict:
        return super()._evaluate_keys(self.transactions, key = "payment_mode")

    @Status._verify_arguments
    def year(self, year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].year == year], key = "payment_mode")

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].year == year and i["transaction_datetime"].month == month], key = "payment_mode")

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> dict:
        return super()._evaluate_keys([i for i in self.transactions if i["transaction_datetime"].date() == date(year, month, day)], key = "payment_mode")