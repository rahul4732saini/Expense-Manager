r"""
Module related to functions used for the backup and restoration of 
transactions, budgets, catagories, payment_modes and user_details.

This exports:

(Class) Backup:
---------------

-   transactions: used for the backup of transactions.
-   budgets: user for the backup of budgets.
-   catagories: used for the backup of catagories.
-   payment_modes: used for the backup of payment modes.
-   user_details: used for the backup of user details.
-   all_data: used for the backup of all data including transactions, budgets, catagories, payment_modes, user_details. 

(Class) Restore:
----------------

-   transactions: used for the restoration of transactions.
-   budgets: user for the restoration of budgets.
-   catagories: used for the restoration of catagories.
-   payment_modes: used for the restoration of payment modes.
-   user_details: used for the restoration of user details.
-   all_data: used for the restoration of all data including transactions, budgets, catagories, payment_modes, user_details. 
"""

try:
    from sys import path
    path.append("..\\Expense Manager")
    
    import json
    import pickle
    import os.path
    import data.info as info
    from functools import wraps
    from dataclasses import dataclass
    from user.details import Manage as user
    import transactions.catagory as catagory
    from budgets.details import Manage as budgets
    from transactions.details import Manage as transactions
    from transactions.payment_mode import Manage as pay_mode
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
class UserDetails:
    user_details: dict

@dataclass
class AllData(Transactions, Budgets, Catagories, PaymentModes, UserDetails):
    ...

class Create:
    def __init__(self, file_name: str, save_directory: str):
        self.__file_name = file_name
        self.__save_directory = save_directory

    @property
    def file_name(self) -> str:
        if len(self.__file_name) not in range(1, 50):
            raise Exception()
        
        return self.__file_name
        
    @property
    def save_directory(self) -> str:
        if not os.path.exists(self.__save_directory):
            raise Exception()
        
        if os.path.exists(f"{self.__save_directory}\\{self.file_name}.bkp"):
            raise Exception()
        
        return self.__save_directory

    def _write_backup(function):

        @wraps(function)
        def wrapper(self) -> None:
            with open("%s\\%s.bkp" % (self.save_directory, self.file_name), 'wb') as file:
                pickle.dump(function(self), file)

        return wrapper

    @_write_backup
    def transactions(self) -> Transactions:
        return Transactions(transactions.get_transactions())

    @_write_backup
    def budgets(self) -> Budgets:
        return Budgets(budgets.get_budgets())

    @_write_backup
    def catagories(self) -> Catagories:
        return Catagories(
            income_details = catagory.Income().get_catagories(),
            expense_details = catagory.Expense().get_catagories()
        )

    @_write_backup
    def payment_modes(self) -> PaymentModes:
        return PaymentModes(pay_mode.get_modes())
    
    @_write_backup
    def user_details(self) -> UserDetails:
        return UserDetails(user.get_details())
    
    @_write_backup
    def all_data(self) -> AllData:
        return AllData(
            transaction_details = transactions.get_transactions(),
            budget_details = budgets.get_budgets(),
            income_details = catagory.Income().get_catagories(),
            expense_details = catagory.Expense().get_catagories(),
            payment_mode_details = pay_mode.get_modes()
        )

class Restore:
    def __init__(self, file_location: str):
        self.__file_location = file_location

    @property
    def file_location(self) -> str:
        if not os.path.exists(self.__file_location):
            raise Exception("0xebkp02us")
        
        base_name = os.path.basename(self.__file_location)

        if base_name.removesuffix(".bkp") == base_name:
            raise Exception()
        
        return self.__file_location

    def _get_data(function):

        @wraps(function)
        def wrapper(self) -> object:
            try:
                with open(self.file_location, 'rb') as file:
                    data: object = pickle.load(file)
            except Exception:
                raise Exception("0xebkp03us")

            try:
                if data.__class__ != function(self):
                    raise Exception
            except Exception:
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
    def user_details(self):
        return UserDetails

    @_get_data
    def all_data(self):
        return AllData
    
class Conflit:

    def transactions(self, transaction_details: Transactions) -> Transactions:
        if transaction_details.__class__ == Transactions:
            return Transactions([i for i in transaction_details if i["transaction_id"] in transactions.get_transactions_id()])
        
        raise Exception()

    def budgets(self, budget_details: Budgets) -> Budgets:
        if budget_details.__class__ == Budgets:
            return Budgets([i for i in budget_details if i["budget_id"] in budgets.get_budgets_id()])
        
        raise Exception()

    def catagories(self, catagory_details: Catagories) -> Catagories:
        if catagory_details.__class__ == Catagories:
            return Catagories(
                income_details = [i for i in catagory_details.income_details if i in catagory.Income().get_catagories()],
                expense_details = [i for i in catagory_details.expense_details if i in catagory.Expense().get_catagories()]
            )
        
        raise Exception()

    def payment_modes(self, payment_modes_details: PaymentModes) -> PaymentModes:
        if payment_modes_details.__class__ == PaymentModes:
            return PaymentModes([i for i in payment_modes_details if i["name"] in pay_mode.get_mode_names()])
        
        raise Exception()

    def user_details(self, user_details: UserDetails) -> UserDetails:
        if user_details.__class__ == UserDetails:
            return UserDetails({key: value for key, value in user_details if (key, value) not in user.get_details().items()})
        
        raise Exception()

    def all_data(self, all_data: AllData) -> AllData:
        if all_data.__class__ == AllData:

            # Capturing the conflicting catagories.
            conflict_catagories: Catagories = self.catagories(
                Catagories(
                    income_details = all_data.income_details,
                    expense_details = all_data.expense_details
                )
            )

            return AllData(
                transaction_details = self.transactions(all_data.transaction_details),
                budget_details = self.budgets(all_data.budget_details),
                income_details = conflict_catagories.income_details,
                expense_details = conflict_catagories.expense_details,
                payment_mode_details = self.payment_modes(all_data.payment_mode_details),
                user_details = self.user_details(all_data.user_details)
            )
        
        raise Exception()
    
class Merge:



    def replace_all(self):
        ...

    def keep_all(self):
        ...

    def replace(self):
        ...

    def skip(self):
        ...

# pending...