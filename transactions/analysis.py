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

    def _get_transactions(self) -> list[dict]:
        return [i for i in Manage().get_transactions() if i["transaction_datetime"] != None]

    def _verify_arguments(function):
        def wrapper(self,
                    year: int,
                    month: int = None,
                    day: int = None):
            
            kwargs = {key: value for key, value in locals().items() if value != None and key not in ["self", "function"]}

            try:
                if (year not in range(1980, 2100)) or (month != None and month not in range(1, 13)):
                    raise Exception
                
                if day != None:
                    date(year, month, day)

                return function(self, **kwargs)
            except Exception:
                raise Exception("0xetrn01an")

        return wrapper

class TransactionNumber(Status):
    def lifetime(self) -> int:
        return Manage().get_transactions().__len__()

    @Status._verify_arguments    
    def year(self, year: int):
        return len([i for i in super()._get_transactions() if i["transaction_datetime"].year == year])

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int:
        return len([i for i in super()._get_transactions() if i["transaction_datetime"].year == year and i["transaction_datetime"].month == month])

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int:
        return len([i for i in super()._get_transactions() if i["transaction_datetime"].date() == date(year, month, day)])

class StatusIncome(Status):
    def __init__(self):
        self._transaction_type = "income" if "Income" in self.__class__.__name__ else "expense"

    def __setattr__(self, name: str, value: Any):
        if name == "transaction_type" and value != ("income" if "Income" in self.__class__.__name__ else "expense"):
            raise Exception("0xegbl0003")

        return super().__setattr__(name, value)
    
    def _get_transactions(self):
        return [i for i in super()._get_transactions() if i["transaction_type"] == self._transaction_type]
    
    def lifetime(self) -> Union[int, float]:    
        return(sum([i["amount"] for i in Manage().get_transactions() if i["transaction_type"] == self._transaction_type]))

    @Status._verify_arguments
    def year(self, year: int) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_datetime"].year == year])
    
    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_datetime"].year == year and i["transaction_datetime"].month == month])
    
    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> Union[str, float]:
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_datetime"].date() == date(year, month, day)])
    
class StatusExpense(StatusIncome, Status):
    def __init__(self):
        super().__init__()

    def lifetime(self) -> Union[int, float]:
        return super().lifetime()
    
    def year(self, year: int) -> Union[int, float]:
        return super().year(year = year)
    
    def month(self,
              month: int,
              year: int) -> Union[int, float]:
        return super().month(month = month, year = year)
    
    def day(self,
            day: int,
            month: int,
            year: int) -> Union[int, float]:
        return super().day(day = day, month = month, year = year)

class Balance(Status):
    def lifetime(self) -> Union[int, float]:
        return StatusIncome().lifetime() - StatusExpense().lifetime()
    
    def year(self, year: int) -> Union[int, float]:
        return StatusIncome().year(year = year) - StatusExpense().year(year = year)
    
    def month(self,
              month: int,
              year: int) -> Union[int, float]:
        return StatusIncome().month(month = month, year = year) - StatusExpense().month(month = month, year = year)
    
    def day(self,
            day: int,
            month: int,
            year: int) -> Union[int, float]:
        return StatusIncome().day(day = day, month = month, year = year) - StatusExpense().day(day = day, month = month, year = year)
    
class AverageIncome(Status):
    def __init__(self):
        self._transaction_type = "income" if "Income" in self.__class__.__name__ else "expense"

    def __setattr__(self, name:str, value: Any):
        if name == "_transaction_type" and value != ("income" if "Income" in self.__class__.__name__ else "expense"):
            raise Exception("0xegbl0003")
        
        return super().__setattr__(name, value)

    def lifetime(self) -> Union[int, float]:
        ...

    @Status._verify_arguments
    def year(self, year: int) -> Union[int, float]:
        ...

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> Union[int, float]:
        ...

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> Union[int, float]:
        ...

class AverageExpense(AverageIncome, Status):
    def __init__(self):
        super().__init__()

    def lifetime(self) -> int:
        return super().lifetime()
    
    @Status._verify_arguments
    def year(self, year: int) -> int:
        return super().year()
    
    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> int:
        return super().month()
    
    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> int:
        return super().day()
    
class CatagoryDistribution(Status):
    def lifetime(self) -> dict:
        ...

    @Status._verify_arguments
    def year(self, year: int) -> dict:
        ...

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> dict:
        ...

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> dict:
        ...

class PaymodeModeDistribution(Status):
    def lifetime(self) -> dict:
        ...

    @Status._verify_arguments
    def year(self, year: int) -> dict:
        ...

    @Status._verify_arguments
    def month(self,
              month: int,
              year: int) -> dict:
        ...

    @Status._verify_arguments
    def day(self,
            day: int,
            month: int,
            year: int) -> dict:
        ...