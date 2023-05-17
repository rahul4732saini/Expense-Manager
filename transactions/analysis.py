try:
    from sys import path
    path.append("..\\Expense Manager")

    from datetime import date
    from details import Manage
    from typing import Union, Any
    from abc import ABC, abstractmethod
except Exception:
    raise Exception("0xegbl0001")

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

class StatusIncome(Status):
    def __init__(self):
        self.transaction_type = "income" if "Income" in self.__class__.__name__ else "expense"

    def __setattr__(self, name: str, value: Any):
        if name == "transaction_type" and value != ("income" if "Income" in self.__class__.__name__ else "expense"):
            raise Exception("0xegbl0003")

        return super().__setattr__(name, value)

    def _verify_arguments(self, function):
        def wrapper(year,
                    month = None,
                    day = None):
            try:
                if (year not in range(1980, 2100)) and (month != None and month not in range(1, 13)):
                    raise Exception
                
                if day != None:
                    date(year, month, day)
            except Exception:
                raise Exception("0xetrn01an")
            
            function()

        return wrapper

    def _get_transactions(self):
        return [i for i in Manage().get_transactions() if i.get("transaction_date") != None and i["transaction_type"] == self.transaction_type]
    
    def lifetime(self) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions()])
    
    @_verify_arguments
    def year(self, year = date.today().year) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"].year == year])
    
    @_verify_arguments
    def month(self,
              month = date.today().month,
              year = date.today().year) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"].year == year and i["transaction_date"].month == month])
    
    @_verify_arguments
    def day(self,
            day = date.today().day,
            month = date.today().month,
            year = date.today().year) -> Union[str, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"] == date(year, month, day)])
    
class StatusExpense(StatusIncome, Status):
    def __init__(self):
        super().__init__()

    def lifetime(self) -> Union[int, float]:
        return super().lifetime()
    
    def year(self, year = date.today().year) -> Union[int, float]:
        return super().year(year)
    
    def month(self,
              month = date.today().month,
              year = date.today().year) -> Union[int, float]:
        return super().month(month, year)
    
    def day(self,
            day = date.today().day,
            month = date.today().month,
            year = date.today().year) -> Union[int, float]:
        return super().day(day, month, year)

class TransactionNumber(Status):
    def lifetime(self) -> int:
        return len(StatusIncome().lifetime()) + len(StatusExpense().lifetime())
    
    def year(self, year = date.today().year) -> int:
        return len(StatusIncome().year(year = year)) + len(StatusExpense().year(year = year))
    
    def month(self,
              month = date.today().month,
              year = date.today().year) -> int:
        return len(StatusIncome().month(month = month, year = year)) + len(StatusExpense().month(month = month, year = year))
    
    def day(self,
            day = date.today().day,
            month = date.today().month,
            year = date.today().year):
        return len(StatusIncome().day(day = day, month = month, year = year)) + len(StatusExpense().day(day = day, month = month, year = year))

class Balance(Status):
    def lifetime(self) -> Union[int, float]:
        return StatusIncome().lifetime() - StatusExpense().lifetime()
    
    def year(self, year = date.today().year) -> Union[int, float]:
        return StatusIncome().year(year = year) - StatusExpense().year(year = year)
    
    def month(self,
              month = date.today().month,
              year = date.today().year) -> Union[int, float]:
        
        return StatusIncome().month(month = month, year = year) - StatusExpense().month(month = month, year = year)
    
    def day(self,
            day = date.today().day,
            month = date.today().month,
            year = date.today().year) -> Union[int, float]:
        
        return StatusIncome().day(day = day, month = month, year = year) - StatusExpense().day(day = day, month = month, year = year)