try:
    from sys import path
    path.append("..\\Expense Manager")

    from budgets.details import manage
    from transactions.catagory import expense
    from typing import Union
except Exception:
    raise Exception("0xegbl0001")

class budgets:
    def __init__(self,
                 budget_range: Union[int, float, range] = None,
                 month: Union[str, range] = None,
                 year: Union[str, range] = None,
                 catagories: Union[str, list] = None):
           
        if all([value == None for key, value in locals().items() if key != "self"]):
            raise Exception()

        if all(
            [
                all([i > 0 for i in [budget_range.start, budget_range.stop, budget_range.step]]) if budget_range.__class__ == range else
                budget_range > 0 if budget_range.__class__ in [int, float] else True if budget_range == None else False,

                month.start in range(1, 13) and month.stop in range(1, 14) and month.step == 1 if month.__class__ == range else
                int(month) in range(1, 13) if month.__class__ == str else True if month == None else False,

                year.start in range(1980, 2100) and year.stop in range(1980, 2101) and year.step == 1 if year.__class__ == range else
                int(year) in range(1980, 2100) if year.__class__ == str else True if year == None else False,
                
                catagories == None or catagories.__class__ in [str, list] and 
                all([i in expense().get_catagories().keys() for i in (catagories if catagories.__class__ == list else [catagories])])
            ]
        ) == False:
            raise Exception()

        self.range = budget_range
        self.month = month
        self.year = year
        self.catagories = catagories