try:
    from sys import path
    path.append("..\\Expense Manager")

    from datetime import date
    from typing import Union
    from details import Manage
except Exception:
    raise Exception("0xegbl0001")

class TransactionNumber:
    def _get_transactions(self):
        return [i for i in Manage().get_transactions() if i .get("transaction_date") != None]

class StatusIncome:
    def __init__(self):
        self.transaction_type = "income" if "Income" in self.__class__.__name__ else "expense"

    def _verify_arguments(self,
                          year,
                          month = None,
                          day = None) -> None:
        try:
            if (year not in range(1980, 2100)) and (month != None or month not in range(1, 13)):
                raise Exception
        
            if day != None:
                date(year, month, day)
        except:
            raise Exception("0xetrn01an")

    def _get_transactions(self):
        return [i for i in Manage().get_transactions() if i.get("transaction_date") != None and i["transaction_type"] == self.transaction_type]
    
    def lifetime(self) -> Union[int, float]:
        return sum([i["amount"] for i in self._get_transactions()])
    
    def year(self, year = date.today().year) -> Union[int, float]:
        self._verify_arguments(year = year)
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"].year == year])
    
    def month(self,
              month = date.today().month,
              year = date.today().year) -> Union[int, float]:
        
        self._verify_arguments(year = year, month = month)
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"].year == year and i["transaction_date"].month == month])
    
    def day(self,
            day = date.today().day,
            month = date.today().month,
            year = date.today().year) -> Union[str, float]:
        
        self._verify_arguments(year = year, month = month, day = day)
        return sum([i["amount"] for i in self._get_transactions() if i["transaction_date"] == date(year, month, day)])
    
class StatusExpense(StatusIncome):
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
    
class Balance:
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