r"""
Module related to functions used
for the filtering of transactions.

(Class) Transactions:
---------------------
-   transaction_id: filters transactions on the basis of the transactions ID provided.
-   datetime_added: filters transactions on the basis of the datetime_added provided.
-   status: filters transactions on the basis of the status provided.
-   amount: filters transactions on the basis of the amount provided.
-   transaction_type: filters transactions on the basis of the transaciton_type provided.
-   payment_mode: filters transactions on the basis of the payment_mode provided.
-   transaction_date: filters transactions on the basis of the transaction_date provided.
-   transaction_datetime: filters transactions on the basis of the transaction_datetime provided.
-   catagory:
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
    import payment_mode as pay_mode
    from datetime import datetime, date
    from catagory import Income, Expense
    import data.pre_requisites as pre_requisites
    from common.objects import DatetimeRange, DateRange
except Exception:
    raise Exception("0xegbl0001")

class Filter:
    def __init__(self):
        self.__filtered_list = Manage().get_transactions()

    @property
    def filtered_list(self):
        return self.__filtered_list

    def transaction_id(self, transaction_id: str | list[str]):
        match transaction_id.__class__.__name__:
            case "str" | "list":
                transaction_id = transaction_id if transaction_id.__class__ == list else [transaction_id]

                if not all((i in Manage().get_transactions_id() for i in transaction_id)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["transaction_id"] in transaction_id, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self
    
    def datetime_added(self, datetime_added: datetime | list[datetime] | DatetimeRange):
        match datetime_added.__class__.__name__:
            case "datetime" | "list":
                datetime_added = datetime_added if datetime_added.__class__ == list else [datetime_added]

                if not all((i.__class__ == datetime for i in datetime_added)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["datetime_added"] in datetime_added, self.__filtered_list))

            case "DatetimeRange":
                if datetime_added.start >= datetime_added.end:
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["datetime_added"] in datetime_added, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self
    
    def status(self, status: str):
        if status not in pre_requisites.TRANSACTION_STATUS:
            raise Exception("0xetrn01fl")
        
        self.__filtered_list = list(filter(lambda trn: trn["status"] == status, self.__filtered_list))
        
        return self

    def amount(self, amount: int | float | list[int | float] | range):
        match amount.__class__.__name__:
            case "int" | "float" | "list":
                amount = amount if amount.__class__ == list else [amount]

                if not all((i.__class__ in (int, float) and i > 0 for i in amount)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["amount"] in amount, self.__filtered_list))

            case "range":
                if amount.start < 0 or amount.start >= amount.stop or amount.step != 1:
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["amount"] in amount, self.__filtered_list))
                
            case _:
                raise Exception("0xetrn01fl")

        return self
    
    def transaction_type(self, transaction_type: str):
        if transaction_type not in pre_requisites.TRANSACTION_TYPES:
            raise Exception("0xetrn01fl")
        
        self.__filtered_list = list(filter(lambda trn: trn["transaction_type"] == transaction_type, self.__filtered_list))
        
        return self
    
    def payment_mode(self, payment_mode: str | list[str]):
        match payment_mode.__class__.__name__:
            case "str" | "list":
                payment_mode = payment_mode if payment_mode.__class__ == list else [payment_mode]

                if not all((i in pay_mode.Manage().get_mode_names() for i in payment_mode)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["payment_mode"] in payment_mode, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self
    
    def transaction_date(self, transaction_date: date | list[date] | DateRange):
        match transaction_date.__class__.__name__:
            case "date" | "list":
                transaction_date = transaction_date if transaction_date.__class__ == list else [transaction_date]

                if not all((i.__class__ == date for i in transaction_date)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["transaction_datetime"].date() in transaction_date, self.__filtered_list))

            case "DateRange":
                if transaction_date.start >= transaction_date.end:
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["transaction_datetime"].date() in transaction_date, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self
    
    def transaction_datetime(self, transaction_datetime: datetime | list[datetime] | DatetimeRange):
        match transaction_datetime.__class__.__name__:
            case "datetime" | "list":
                transaction_datetime = transaction_datetime if transaction_datetime.__class__ == list else [transaction_datetime]

                if not all((i.__class__ == datetime for i in transaction_datetime)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["transaction_datetime"] in transaction_datetime, self.__filtered_list))

            case "DatetimeRange":
                if transaction_datetime.start >= transaction_datetime.end:
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["transaction_datetime"] in transaction_datetime, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self

    def catagory(self, catagory: str | list[str], transaction_type: str):
        if transaction_type not in pre_requisites.TRANSACTION_TYPES:
            raise Exception("0xetrn01fl")
        
        catagory_type = Income() if transaction_type == "income" else Expense()

        match catagory.__class__.__name__:
            case "str" | "list":
                catagory = catagory if catagory.__class__ == list else [catagory]

                if not all((i in catagory_type.get_catagories() for i in catagory)):
                    raise Exception("0xetrn01fl")
                
                self.__filtered_list = list(filter(lambda trn: trn["catagory"] in catagory, self.__filtered_list))

            case _:
                raise Exception("0xetrn01fl")

        return self