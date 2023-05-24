r"""
Module related to function used
for the filtering of budgets.

(Class) Budgets:
----------------
-   filter_budget_id: filters budgets on the basis of budgets_id provided.
-   filter_datetime_added: filters budgets on the basis of the datetime provided.
-   filter_range: filter budgets on the basis of the range provided.
-   filter_active_month: filters budgets on the basis of the active_month provided.
-   filter_catagory: filters budgets on the basis of the catagories provided.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
    from datetime import date, datetime
    from transactions.catagory import Expense
    from objects.datetime_range import DateRange, DatetimeRange
except Exception:
    raise Exception("0xegbl0001")

class Budgets:
    def __init__(self):
        self.__filtered_list: list = Manage().get_budgets()

    @property
    def filtered_list(self) -> list[dict]:
        return self.__filtered_list
    
    @filtered_list.setter
    def filtered_list(self, value) -> None:
        if value.__class__ != list or not all([i in Manage().get_budgets() for i in value]):
            raise Exception("0xegbl0003")
        
        self.__filtered_list = value

    def filter_budget_id(self, budget_id: str | list[str]):
        match budget_id.__class__.__name__:
            case "str" | "list":
                budget_id = budget_id if budget_id.__class__ == list else [budget_id]

                if not all([i in Manage().get_budgets_id() for i in budget_id]):
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["budget_id"] in budget_id, self.filtered_list))

            case _:
                raise Exception()

        return self

    def filter_datetime_added(self, datetime_added: datetime | list[datetime] | DatetimeRange):
        match datetime_added.__class__.__name__:
            case "datetime" | "list":
                datetime_added = datetime_added if datetime_added.__class__ == list else [datetime_added]

                if not all([i < datetime.today() and i.year >= 1980 for i in datetime_added]):
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["datetime_added"] in datetime_added, self.filtered_list))

            case "DatetimeRange":
                if not all([i.year in range(1980, 2100) for i in [datetime_added.start, datetime_added.end]]) or datetime_added.start == datetime_added.end:
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["datetime_added"] in datetime_added, self.filtered_list))

            case _:
                raise Exception()

        return self

    def filter_range(self, budget_range: int | list[int] | range):
        match budget_range.__class__.__name__:
            case "int" | "list":
                budget_range = budget_range if budget_range.__class__ == list else [budget_range]

                if not all([i > 0 for i in budget_range]):
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["range"] in budget_range, self.filtered_list))

            case "range":
                if budget_range.start < 0 or budget_range.stop <= budget_range.start or budget_range.step != 1:
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["range"] in budget_range, self.filtered_list))

            case _:
                raise Exception()

        return self

    def filter_active_month(self, active_month: date | list[date] | DateRange):
        match active_month.__class__.__name__:
            case "date" | "list":
                active_month = active_month if active_month.__class__ == list else [active_month]

                if not all([i.year in range(1980, 2100) for i in active_month]):
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: date(bgt["year"], bgt["month"], 1) in active_month, self.filtered_list))

            case "DateRange":
                if not all([i.year in range(1980, 2100) for i in (active_month.start, active_month.end)]) or active_month.start == active_month.end:
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: date(bgt["year"], bgt["month"], 1) in active_month, self.filtered_list))

            case _:
                raise Exception()

        return self
    
    def filter_catagory(self, catagory: str | list[str]):
        match catagory.__class__.__name__:
            case "str" | "list":
                catagory = catagory if catagory.__class__ == list else [catagory]

                if not all([i in Expense().get_catagories() for i in catagory]):
                    raise Exception()
                
                self.filtered_list = list(filter(lambda bgt: bgt["catagories"] in catagory, self.filtered_list))

            case "NoneType":
                self.filtered_list = list(filter(lambda bgt: bgt["catagories"] == None, self.filtered_list))

            case _:
                raise Exception()                

        return self