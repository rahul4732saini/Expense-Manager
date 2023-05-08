from sys import path
path.append("..\\Expense Manager")

import os
from typing import Union
from transactions.details import manage
from transactions.catagory import income, expense
import data.pre_requisites as pre_requisites

class transactions:
    def __init__(self,
                 transaction_id: str = None,
                 amount: Union[int ,float , range, list] = None,
                 transaction_type: str = None,
                 transaction_mode: Union[str, list] = None,
                 catagories: Union[str, list] = None,
                 day: Union[str, range, list] = None,
                 month: Union[str, range, list] = None,
                 year: Union[str, range, list] = None):
        
        if all([value is None for key, value in locals().items() if key != "self"]):
            raise Exception()
        
        if all(
            [
                transaction_id == None or transaction_id in manage().get_transactions_id(),

                amount > 0 if amount.__class__ in [int, float] else
                all([i > 0 for i in ([amount.start, amount.stop] if amount.__class__ == range else amount)]) if
                amount.__class__ in [range, list] else True if amount == None else False,
                amount.step == 1 if amount.__class__ == range else True,

                transaction_type in pre_requisites.TRANSACTION_TYPES,
                transaction_mode.__class__ == str,
            ]
        ) == False:
            raise Exception()

        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_mode = transaction_mode
        self.day = day
        self.month = month
        self.year = year
        self.catagories = catagories