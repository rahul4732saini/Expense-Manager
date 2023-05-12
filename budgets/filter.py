try:
    from sys import path
    path.append("..\\Expense Manager")

    from budgets.details import manage
    from transactions.catagory import expense
    from typing import Union
    from datetime import date, time
except Exception:
    raise Exception("0xegbl0001")

class budgets:
    def __init__(self,
                 budget_id: Union[str, list] = None,
                 budget_range: Union[int, float, list, range] = None,
                 month: Union[str, range, list] = None,
                 year: Union[str, range, list] = None,
                 catagories: Union[str, list] = None):
           
        if all([value == None for key, value in locals().items() if key != "self"]):
            raise Exception()

        self.budget_id = budget_id
        self.range = budget_range
        self.month = month
        self.year = year
        self.catagories = catagories

        self._check_validity()

    def _check_validity(self) -> None:
        if all(
            [
                #Validating budget_id
                ...,

                # Validating budget_range
                self.range == None or (self.range > 0 if self.range.__class__ in [int, float] else
                all([i > 0 if i.__class__ in [int, float] else False for i in self.range]) if self.range.__class__ == list else
                self.range.start >= 0 and self.range.stop > 0 and self.range.start <= self.range.stop and self.range.step == 1 if self.range.__class__ == range
                else False),

                # Validating month
                self.month == None or (int(self.month) in range(1, 13) if self.month.__class__ == str and self.month.isdigit() else
                all([int(i) in range(1, 13) if i.__class__ == str and i.isdigit() else False for i in self.month]) if self.month.__class__ == list else
                self.month.start in range(1, 13) and self.month.stop in range(1, 14) and self.month.step == 1 if self.month.__class__ == range
                else False),

                # Validating year
                self.year == None or (int(self.year) in range(1980, 2100) if self.year.__class__ == str and self.year.isdigit() else
                all([int(i) in range(1980, 2100) if i.__class__ == str and i.isdigit() else False for i in self.year]) if self.year.__class__ == list else
                self.year.start in range(1980, 2100) and self.year.stop in range(1980, 2101) and self.year.step == 1 if self.year.__class__ == range
                else False),

                # Validating catagories
                self.catagories == None or (self.catagories in expense().get_catagories() if self.catagories.__class__ == str else
                all([i in expense().get_catagories() for i in self.catagories]) if self.catagories.__class__ == list
                else False)
            ]
        ) == False:
            raise Exception()

    def filter(self) -> list:

        # Filtering budget_range
        filtered_list = [
            i for i in manage().read_budgets() if self.range.__class__ in [int, float] and i.get("range") == self.range
            or self.range.__class__ in [list, range] and i.get("range") in self.range
        ] if self.range != None else manage().read_budgets()

        # Filtering budget year
        filtered_list = [
            i for i in filtered_list if self.year.__class__ == str and i.get("year") == self.year
            or self.year.__class__ in [list, range] and i.get("year") in self.year
        ] if self.year != None else filtered_list

        # Filter budget catagories
        filtered_list = [
            i for i in filtered_list if self.catagories.__class__ == str and self.catagories in i.get("catagories").keys()
            or self.range.__class__ == list and all([i in i.get("catagories").keys() for i in self.catagories])
        ] if self.catagories != None else filtered_list

        return filtered_list