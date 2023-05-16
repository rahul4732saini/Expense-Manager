try:
    from sys import path
    path.append("..\\Expense Manager")

    from typing import Union
    from datetime import date, time
    from budgets.details import manage
    from transactions.catagory import expense
except Exception:
    raise Exception("0xegbl0001")

class budgets:
    def __init__(self,
                 budget_id: Union[str, list[str]] = None,
                 date_added: Union[date, list[date]] = None,
                 time_added: Union[time, list[time]] = None,
                 budget_range: Union[int, float, list, range] = None,
                 month: Union[str, range, list[str]] = None,
                 year: Union[str, range, list[str]] = None,
                 catagories: Union[str, list[str]] = None):
           
        if all([value == None for key, value in locals().items() if key != "self"]):
            raise Exception()

        self.budget_id = budget_id
        self.date_added = date_added
        self.time_added = time_added
        self.range = budget_range
        self.month = month
        self.year = year
        self.catagories = catagories

        self._check_validity()

    def _check_validity(self) -> None:
        date_range: list[date] = [date(1979, 12, 31), date(2100, 1, 1)]

        if all(
            [
                # Verifying budget_id
                self.budget_id == None or (self.budget_id in manage().get_budgets_id() if self.budget_id.__class__ == str else False),

                # Verifying date_added
                self.date_added == None or (self.date_added > date(1979, 12, 31) and self.date_added < date(2100, 1, 1) if self.date_added.__class__ == date else
                all([i > date_range[0] and i < date_range[1] if i.__class__ == date else False for i in self.date_added]) if self.date_added.__class__ == list
                else False),

                # Verifying time_added
                self.time_added == None or self.time_added.__class__ == time or
                (all([i.__class__ == time for i in self.time_added]) if self.time_added.__class__ == list else False),

                # Verifying budget_range
                self.range == None or (self.range > 0 if self.range.__class__ in [int, float] else
                all([i > 0 if i.__class__ in [int, float] else False for i in self.range]) if self.range.__class__ == list else
                self.range.start >= 0 and self.range.stop > 0 and self.range.start <= self.range.stop and self.range.step == 1 if self.range.__class__ == range
                else False),

                # Verifying month
                self.month == None or (int(self.month) in range(1, 13) if self.month.__class__ == str and self.month.isdigit() else
                all([int(i) in range(1, 13) if i.__class__ == str and i.isdigit() else False for i in self.month]) if self.month.__class__ == list else
                self.month.start in range(1, 13) and self.month.stop in range(1, 14) and self.month.step == 1 if self.month.__class__ == range
                else False),

                # Verifying year
                self.year == None or (int(self.year) in range(1980, 2100) if self.year.__class__ == str and self.year.isdigit() else
                all([int(i) in range(1980, 2100) if i.__class__ == str and i.isdigit() else False for i in self.year]) if self.year.__class__ == list else
                self.year.start in range(1980, 2100) and self.year.stop in range(1980, 2101) and self.year.step == 1 if self.year.__class__ == range
                else False),

                # Verifying catagories
                self.catagories == None or (self.catagories in expense().get_catagories() if self.catagories.__class__ == str else
                all([i in expense().get_catagories() for i in self.catagories]) if self.catagories.__class__ == list
                else False)
            ]
        ) == False:
            raise Exception()

    def filter(self) -> list:
        # Filter budget_id
        filtered_list = [
            i for i in manage().read_budgets() if self.budget_id.__class__ == str and i.get("budget_id") == self.budget_id
            or self.budget_id.__class__ == list and i.get("budget_id") in self.budget_id
        ] if self.budget_id != None else manage().read_budgets()

        # Filter date_added
        filtered_list = [
            i for i in manage().read_budgets() if self.budget_id.__class__ == date and i.get("budget_id")
        ]

        # Filtering budget_range
        filtered_list = [
            i for i in filtered_list if self.range.__class__ in [int, float] and i.get("range") == self.range
            or self.range.__class__ in [list, range] and i.get("range") in self.range
        ] if self.range != None else filtered_list

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