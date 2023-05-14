from sys import path
path.append("..\\Expense Manager")

from time import strptime
from typing import Union
try:
    from details import manage
except Exception:
    raise Exception("0xegbl0001")

class status_income:
    type = "income"

    def _check_validity(self,
                       year,
                       month = None,
                       day = None) -> None:
        try:
            if all(
                [
                    year.__class__ == str,
                    int(year) in range(1980, 2100),
                    month == None or month.__class__ == str and int(month) in range(1,13),
                    day == None or day.__class__ == str and bool(strptime("%s-%s-%s" % (day, month, year), "%d-%m-%Y"))
                ]
            ) == False:
                raise Exception
        except Exception:
            raise Exception("0xetrn01an")

    def _filter_transactions(self):
        return [i for i in manage().read_transactions() if i.get("transaction_date") != None]

    def yearly(self, year:str, type = "income") -> Union[int, float]:
        self._check_validity(year = year)
        return sum([i.get('amount') for i in self._filter_transactions() if i.get('transaction_date')[-4:] == year and i.get('transaction_type') == type])
    
    def monthly(self, month:str, year:str, type = "income") -> Union[int ,float]:
        self._check_validity(year = year, month = month)
        month = "0%s" % (month) if month.__len__() == 1 else month

        return sum([i.get('amount') for i in self._filter_transactions() if i.get('transaction_date')[-7:] == "%s-%s" % (month, year) and i.get('transaction_type') == type])
    
    def daily(self,
              day:str,
              month:str,
              year:str,
              type = "income") -> Union[int, float]:
        self._check_validity(year = year, month = month, day = day)
        month = "0%s" % (month) if month.__len__() == 1 else month
        day = "0%s" % (day) if day.__len__() == 1 else day

        return sum([i.get('amount') for i in self._filter_transactions() if i.get('transaction_date') == "%s-%s-%s" % (day, month, year) and i.get('transaction_type') == type])
    
class status_expense(status_income):
    def yearly(self, year:str) -> Union[int, float]:
        return super().yearly(year = year, type = "expense")
    
    def monthly(self, month:str, year:str) -> Union[int, float]:
        return super().monthly(month = month, year = year, type = "expense")
    
    def daily(self, day:str, month:str, year:str) -> Union[int, float]:
        return super().daily(day = day, month = month, year = year, type = "expense")
    
class Balance:
    def yearly(self, year:str):
        return status_income().yearly(year = year) - status_expense().yearly(year = year)

    def monthly(self, month:str, year:str):
        return status_income().monthly(year = year, month = month) - status_expense().monthly(year = year, month = month)
    
    def daily(self, day:str, month:str, year:str):
        return status_income().daily(year = year, month = month, day = day) - status_expense().daily(year = year, month = month, day = day)