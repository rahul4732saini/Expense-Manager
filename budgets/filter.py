r"""
Module related to function used
for the filtering of budgets.

(Class) Filter:
----------------
-   budget_id: filters budgets on the basis of budgets_id provided.
-   datetime_added: filters budgets on the basis of the datetime provided.
-   range: filter budgets on the basis of the range provided.
-   active_month: filters budgets on the basis of the active_month provided.
-   catagory: filters budgets on the basis of the catagories provided.
-   under_limit: filters budgets which are under limit.
-   upper_limit: filters budget which are upper limit.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from budgets.details import Manage
    from datetime import date, datetime
    import transactions.analysis as analysis
    from transactions.catagory import Expense
    from common.objects import DateRange, DatetimeRange

except Exception:
    raise Exception("0xegbl0001")

class Filter:
    def __init__(self):
        self.__filtered_list: list = Manage().get_budgets()

    @property
    def filtered_list(self) -> list[dict]:
        return self.__filtered_list

    def budget_id(self, budget_id: str | list[str]):
        match budget_id.__class__.__name__:
            case "str" | "list":
                budget_id = budget_id if budget_id.__class__ == list else [budget_id]

                if not all((i in Manage().get_budgets_id() for i in budget_id)):
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: bgt["budget_id"] in budget_id, self.__filtered_list))

            case _:
                raise Exception("0xebgt01fl")

        return self

    def datetime_added(self, datetime_added: datetime | list[datetime] | DatetimeRange):
        match datetime_added.__class__.__name__:
            case "datetime" | "list":
                datetime_added = datetime_added if datetime_added.__class__ == list else [datetime_added]

                if not all((i.__class__ == datetime for i in datetime_added)):
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: bgt["datetime_added"] in datetime_added, self.__filtered_list))

            case "DatetimeRange":
                if datetime_added.start >= datetime_added.end:
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: bgt["datetime_added"] in datetime_added, self.__filtered_list))

            case _:
                raise Exception("0xebgt01fl")

        return self

    def range(self, budget_range: int | float | list[int | float] | range):
        match budget_range.__class__.__name__:
            case "int" | "float" | "list":
                budget_range = budget_range if budget_range.__class__ == list else [budget_range]

                if not all((i.__class__ in (int, float) and i > 0 for i in budget_range)):
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: bgt["range"] in budget_range, self.__filtered_list))

            case "range":
                if budget_range.start < 0 or budget_range.stop <= budget_range.start or budget_range.step != 1:
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: bgt["range"] in budget_range, self.__filtered_list))

            case _:
                raise Exception("0xebgt01fl")

        return self

    def active_month(self, active_month: date | list[date] | DateRange):
        match active_month.__class__.__name__:
            case "date" | "list":
                active_month = active_month if active_month.__class__ == list else [active_month]

                if not all((i.__class__ == date for i in active_month)):
                    raise Exception("0xebgt01fl")
                
                self.__filtered_list = list(filter(lambda bgt: date(bgt["year"], bgt["month"], 1) in active_month, self.__filtered_list))

            case "DateRange":
                if active_month.start >= active_month.end:
                    raise Exception("0xebgt01fl")
                
                # Function used for filtering budgets on the basis of the month provided.
                validity_check = lambda bgt: all((i["month"] == bgt["month"] and i["year"] == bgt["year"] for i in active_month))

                self.__filtered_list = list(filter(validity_check, self.__filtered_list))

            case _:
                raise Exception("0xebgt01fl")

        return self
    
    def catagory(self, catagory: str | list[str]):
        match catagory.__class__.__name__:
            case "str" | "list":
                catagory = catagory if catagory.__class__ == list else [catagory]

                if not all((i == None or i in Expense().get_catagories() for i in catagory)):
                    raise Exception("0xebgt01fl")

                # Function used for filtering bugets on the basis of catagories provided.
                validity_check = lambda bgt: bgt["catagories"] in catagory or all([i in catagory for i in bgt["catagories"]])

                self.__filtered_list = list(filter(validity_check, self.__filtered_list))

            case "NoneType":
                self.__filtered_list = list(filter(lambda bgt: bgt["catagories"] == None, self.__filtered_list))

            case _:
                raise Exception("0xebgt01fl")     

        return self
    
    def under_limit(self):

        # Function for filtering budgets on the basis of under_limit.
        validity_check = lambda bgt: bgt["range"] >= analysis.StatusExpense().month(month = bgt["month"], year = bgt["year"])
        self.__filtered_list =  list(filter(validity_check, self.__filtered_list))

        return self
    
    def upper_limit(self):

        # Function for filtering budgets on the basis of upper limit.
        validity_check = lambda bgt: bgt["range"] <= analysis.StatusExpense().month(month = bgt["month"], year = bgt["year"])
        self.__filtered_list =  list(filter(validity_check, self.__filtered_list))

        return self