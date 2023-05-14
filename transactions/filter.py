from sys import path
path.append("..\\Expense Manager")

from datetime import date, time
from typing import Union
from datetime import date, time
import data.pre_requisites as pre_requisites
from details import manage
from catagory import income, expense

class transactions:
    def __init__(self,
                 transaction_id: Union[str, list[str]] = None,
                 date_added: Union[date, list[date]] = None,
                 time_added: Union[time, list[time]] = None,
                 status: str = None,
                 amount: Union[int, float, list, range] = None,
                 transaction_type: str = None,
                 transaction_mode: Union[str, list[str]] = None,
                 catagories: Union[str, list[str]] = None):
        
        if all([value == None for key, value in locals().items() if key != "self"]):
            raise Exception("1")
        
        self.transaction_id = transaction_id
        self.date_added = date_added
        self.time_added = time_added
        self.status = status
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_mode = transaction_mode
        self.catagories = catagories

        self._check_validity()

    def _check_validity(self) -> None:
        date_range: list[date] = [date(1979, 12, 31), date(2100, 1, 1)]

        if all(
            [
                # Validating transaction ID
                self.transaction_id == None or (self.transaction_id in manage().get_transactions_id() if self.transaction_id.__class__ == str else
                all([i in manage().get_transactions_id() for i in self.transaction_id]) if self.transaction_id.__class__ == list
                else False),

                # Validating date_added
                self.date_added == None or (self.date_added > date(1979, 12, 31) and self.date_added < date(2100, 1, 1) if self.date_added.__class__ == date else
                all([i > date_range[0] and i < date_range[1] if i.__class__ == date else False for i in self.date_added]) if self.date_added.__class__ == list
                else False),

                # Validating time_added
                self.time_added == None or self.time_added.__class__ == time or
                (all([i.__class__ == time for i in self.time_added]) if self.time_added.__class__ == list else False),

                # Validating status
                self.status == None or self.status in pre_requisites.STATUS,

                # Validating amount
                self.amount == None or (self.amount > 0 if self.amount.__class__ in [int ,float] else
                all([i > 0 if i.__class__ in [int, float] else False for i in self.amount]) if self.amount.__class__ == list else
                self.amount.start >= 0 and self.amount.stop > 0 and self.amount.step == 1 if self.amount.__class__ == range
                else False),

                # Validating transaction type
                self.transaction_type == None or self.transaction_type in pre_requisites.TRANSACTION_TYPES,

                # Validating transaction mode
                self.transaction_mode == None or self.transaction_mode.__class__ == str,

                # Validating catagories
                self.catagories == None or ((self.catagories in income().get_catagories() if self.transaction_type == "income" else
                self.catagories in expense().get_catagories() if self.transaction_type == "expense" else False) if self.catagories.__class__ == str else
                all(
                    [
                        i in income().get_catagories() if self.transaction_type == "income" else
                        i in expense().get_catagories() if self.transaction_type == "expense" else False
                        for i in self.catagories
                    ]
                ) if self.catagories.__class__ == list else False)
            ]
        ) == False:
            raise Exception("2")
        
    def filter(self) -> None:
        ...