r"""
Module related to function used
for the filtering of budgets.

(Class) Budgets:
----------------
-   filter_budget_id:
-   filter_datetime_added:
-   filter_range:
-   filter_active_month:
-   filter_catagory:
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from typing import Union
    from details import Manage
    from datetime import date, datetime
    from transactions.catagory import Expense
    from objects.datetime_range import DateRange, DatatimeRange
except Exception:
    raise Exception("0xegbl0001")

class Budgets:
    def __init__(self):
        self.__filtered_list: list = Manage().get_budgets()

    @property
    def filetered_list(self) -> list[dict]:
        return self.__filtered_list
    
    def filter_budget_id(self, budget_id: str | list[str]):

        def _verify_arguments(budget_id):
            if budget_id.__class__ not in [str, list]:
                raise Exception
        
            match budget_id.__class__:
                case "str":
                    if budget_id not in Manage().get_budgets_id():
                        raise Exception
                    
                case "list":
                    if len(budget_id) != len(set(budget_id)):
                        raise Exception
                    
                    if not any([i in Manage().get_budgets_id() for i in budget_id]):
                        raise Exception
                    
        _verify_arguments(budget_id)

        return self

    def filter_datetime_added(self, datetime_added: datetime | list[datetime] | DatatimeRange):

        def _verify_argumentss(datetime_added):
            if datetime_added.__class__ not in [datetime, list, DatatimeRange]:
                raise Exception
            
            match datetime_added.__class__:
                case "datetime" | "list":
                    if not any([i < datetime.today() and i.year >= 1980 for i in (datetime_added if datetime_added.__class__ == list else [datetime_added])]):
                        raise Exception
                    
                case "DatatimeRange":
                    if not any([i.year in range(1980, 2100) for i in [datetime_added.start, datetime_added.end]]):
                        raise Exception
                    
        _verify_argumentss(datetime_added)

        return self

    def filter_range(self, budget_range: Union[int, list[int], range]):

        def _verify_arguments(budget_range):
            if budget_range.__class__ not in [int, list, range]:
                raise Exception
            
            match budget_range.__class__:
                case "int" | "list":
                    if not any(i > 0 for i in (budget_range if budget_range.__class__ == list else [budget_range])):
                        raise Exception()
                    
                case "range":
                    if budget_range.start <= 0 or budget_range.stop <= budget_range.start or budget_range.step != 1:
                        raise Exception()
                    
        _verify_arguments(budget_range)

        return self

    def filter_active_month(self, active_month: date | list[date] | DateRange):

        def _verify_arguments(active_month):
            if active_month.__class__ not in [date, list, DateRange]:
                raise Exception
            
            match active_month.__class__:
                case "date" | "list":
                    if not any([i.year in range(1980, 2100) for i in (active_month if active_month.__class__ == list else [active_month])]):
                        raise Exception
                    
                case "DateRange":
                    if not any([i.year in range(1980, 2100) for i in [active_month.start, active_month.end]]):
                        raise Exception
                    
        _verify_arguments(active_month)

        return self
    
    def filter_catagory(self, catagory: str | list[str]):
        
        def _verify_arguments(catagory):
            if catagory.__class__ in [str, list]:
                raise Exception

            if not all([i in Expense().get_catagories() for i in (catagory if catagory.__class__ == list else catagory)]):
                        raise Exception
            
        _verify_arguments(catagory)

        return self