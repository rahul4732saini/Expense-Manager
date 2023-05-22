r"""
Module related to functions used
for the filtering of transactions.

(Class) Transactions:
---------------------
-   filter_transaction_id:
-   filter_datetime_added:
-   filter_status:
-   filter_amount:
-   filter_transaction_type:
-   filter_payment_mode:
-   filter_transaction_datetime:
-   filter_catagory:
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
    from datetime import datetime
    import payment_mode as pay_mode
    from catagory import Income, Expense
    import data.pre_requisites as pre_requisites
    from objects.datetime_range import DatatimeRange
except Exception:
    raise Exception("0xegbl0001")

class Transactions:
    def __init__(self):
        self.__filtered_list = Manage().get_transactions()

    @property
    def filtered_list(self):
        return self.__filtered_list

    def filter_transaction_id(self, transaction_id: str | list[str]):

        def verify_arguments(transaction_id):
            if transaction_id.__class__ not in [str, list]:
                raise Exception()
            
            if not all([i in Manage().get_transactions_id() for i in (transaction_id if transaction_id.__class__ == list else [transaction_id])]):
                raise Exception()
            
        verify_arguments(transaction_id)

        return self
    
    def filter_datetime_added(self, datetime_added: datetime | list[datetime] | DatatimeRange):

        def verify_arguments(datetime_added):
            if datetime_added.__class__ not in [datetime, list, DatatimeRange]:
                raise Exception()
            
            match datetime_added.__class__.__name__:
                case "datetime" | "list":
                    if not all([i.year in range(1980, 2100) for i in (datetime_added if datetime_added.__class__ == list else [datetime_added])]):
                        raise Exception()
                    
                case "DatetimeRange":
                    if not all([i.year in range(1980, 2100) for i in [datetime_added.start, datetime_added.end]]):
                        raise Exception()
                    
        verify_arguments(datetime_added)

        return self
    
    def filter_amount(self, amount: int | list[int] | range):

        def verify_arguments(amount):
            if amount.__class__ not in [int, list, range]:
                raise Exception()
            
            match amount.__class__.__name__:
                case "int" | "list":
                    if not all([i > 0 for i in (amount if amount.__class__ == list else [amount])]):
                        raise Exception()
                    
                case "range":
                    if not (amount.start >= 0 and amount.stop > amount.start and amount.step == 1):
                        raise Exception()
                    
        verify_arguments(amount)

        return self
    
    def filter_transaction_type(self, transaction_type: str):
        if transaction_type not in ["income", "expense"]:
            raise Exception()
        
        return self
    
    def filter_payment_mode(self, payment_mode: str | list[str]):
        
        def verify_arguments(payment_mode):
            if payment_mode.__class__ not in [str, list]:
                raise Exception()
            
            if not all([i in pay_mode.Manage().get_mode_names() for i in (payment_mode if payment_mode.__class__ == list else [payment_mode])]):
                raise Exception()
            
        verify_arguments(payment_mode)

        return self
    
    def filter_status(self, status: str):
        if status not in pre_requisites.TRANSACTION_KEYS:
            raise Exception()
        
        return self
    
    def filter_catagory(self, catagory: str | list[str], transaction_type: str):
        
        def verify_arguments(catagory, transaction_type):
            if catagory.__class__ not in [str, list]:
                raise Exception()
        
            if transaction_type not in ["income", "expense"]:
                raise Exception()
        
            catagory_file = Income() if transaction_type == "income" else Expense()

            if not all([i in catagory_file.get_catagories() for i in (catagory if catagory.__class__ == list else [catagory])]):
                raise Exception()
            
        verify_arguments(catagory, transaction_type)

        return self
    
    def filter_transaction_datetime(self, transaction_datetime: datetime | list[datetime] | DatatimeRange):
        
        def verify_arguments(transaction_datetime):
            if transaction_datetime.__class__ not in [datetime, list, DatatimeRange]:
                raise Exception()
            
            match transaction_datetime.__class__.__name__:
                case "datetime" | "list":
                    if not all([i.year in range(1980, 2100) for i in (transaction_datetime if transaction_datetime.__class__ == list else transaction_datetime)]):
                        raise Exception()
                    
                case "DatatimeRange":
                    if not all([i.year in range(1980, 2100) for i in [transaction_datetime.start, transaction_datetime.end]]):
                        raise Exception()

        verify_arguments(transaction_datetime)

        return self
    
# pending...