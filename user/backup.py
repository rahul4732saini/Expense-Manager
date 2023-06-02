r"""
Module related to functions used for the backup and restoration of 
transactions, budgets, catagories, payment_modes and user_details.

This exports:

(Class) Backup:
---------------

-   transactions:
-   budgets:
-   catagories:
-   payment_modes:
-   all_data:

(Class) Restore:
----------------

-   transactions:
-   budgets:
-   catagories:
-   payment_modes:
-   all_data:
"""

try:
    from sys import path
    path.append("..\\Expense Manager")
    
    import pickle
    import os.path
    from functools import wraps
    import user.details as user
    from dataclasses import dataclass
    import budgets.details as budgets
    import transactions.details as transactions
    import transactions.catagory as catagory
    import transactions.payment_mode as pay_mode
except Exception:
    raise Exception("0xegbl0001")

@dataclass
class Transactions:
    transaction_details: list[dict]

@dataclass
class Budgets:
    budget_details: list[dict]

@dataclass
class Catagories:
    income_details: dict
    expense_details: dict

@dataclass
class PaymentModes:
    payment_mode_details: list[dict]

@dataclass
class AllData(Transactions, Budgets, Catagories, PaymentModes):
    ...

class Create:
    def _write_backup(function) -> None:

        @wraps(function)
        def wrapper(self,
                    file_name: str,
                    save_location: str):
            if not os.path.exists(save_location):
                raise Exception("0xebkp01us")
        
            if len(file_name) not in range(1, 50):
                raise Exception("0xebkp01us")
        
            with open("%s\\%s.pickle" % (save_location, file_name), 'wb') as file:
                pickle.dump(function(self), file)

        return wrapper

    @_write_backup
    def transactions(self) -> None:
        return Transactions(transactions.Manage().get_transactions())

    @_write_backup
    def budgets(self) -> None:
        return Budgets(budgets.Manage().get_budgets())

    @_write_backup
    def catagories(self):
        return Catagories(
            income_details = catagory.Income().get_catagories(),
            expense_details = catagory.Expense().get_catagories()
        )

    @_write_backup
    def payment_modes(self):
        return PaymentModes(pay_mode.Manage().get_modes())
    
    @_write_backup
    def all_data(self) -> None:
        return AllData(
            transaction_details = transactions.Manage().get_transactions(),
            budget_details = budgets.Manage().get_budgets(),
            income_details = catagory.Income().get_catagories(),
            expense_details = catagory.Expense().get_catagories(),
            payment_mode_details = pay_mode.Manage().get_modes()
        )
    
class Restore:
    def __init__(self, file_location: str):
        self.__file_location = file_location

    @property
    def file_location(self):
        if not os.path.exists(self.__file_location):
            raise Exception("0xebkp02us")
        
        return self.__file_location
    
    def _get_data(function):

        @wraps(function)
        def wrapper(self) -> list[dict] | dict:

            try:
                with open(self.file_location, 'rb') as file:
                    data: object = pickle.load(file)
            except Exception:
                raise Exception("0xebkp03us")

            if data.__class__ != function(self):
                raise Exception("0xebkp04us")
            
            return data
        
        return wrapper

    @_get_data
    def transactions(self):
        return Transactions

    @_get_data
    def budgets(self):
        return Budgets

    @_get_data
    def catagories(self):
        return Catagories

    @_get_data
    def payment_modes(self):
        return PaymentModes

    @_get_data
    def all_data(self):
        return AllData