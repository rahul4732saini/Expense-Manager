r"""
This module contains important datatypes
used in the filtering of budgets and transactions.

This exports:

(DataType) DateRange:
---------------------

-  Parameters:

start_date: datetime.date = starting date of the range.
end_date: datetime.date = ending date of the range.

(DataType) DatetimeRange:
-------------------------

-  Parameters:

start_datetime: datetime.datetime = starting datetime of the range.
end_datetime: datetime.datetime = ending datetime of the range.
"""

try:
    from dataclasses import dataclass
    from datetime import date, datetime
except:
    raise Exception("0xegbl0001")

@dataclass
class Transaction:
    transaction_id: str
    status: str
    datetime_added: datetime
    amount: int | float
    transaction_type: str
    payment_mode: str
    catagory: str
    transaction_datetime: datetime
    description: str | None
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        
        return self.transaction_id == other.transaction_id

@dataclass
class Transactions:
    transactions: set[Transaction]

@dataclass
class Budget:
    budget_id: str
    datetime_added: datetime
    range: int | float
    month: str
    year: str
    catagories: dict | None

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Budget):
            return False
        
        return self.budget_id == other.budget_id

@dataclass
class Budgets:
    budget_details: set[Budget]

@dataclass
class Catagory:
    name: str
    color: str

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Catagory):
            return False
        
        return self.name == other.name

@dataclass
class Catagories:
    income_catagories: set[Catagory]
    expense_catagories: set[Catagory]

@dataclass
class PaymentMode:
    name: str
    color: str
    catagory: str
    initial_balance: int | float

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other: object):
        if not isinstance(other, PaymentMode):
            return False
        
        return self.name == other.name

@dataclass
class PaymentModes:
    payment_modes: set[PaymentMode]

@dataclass
class User:
    first_name: str
    middle_name: str
    last_name: str
    email_id: str
    region: str
    date_of_birth: date

@dataclass
class AllData:
    transactions: Transaction
    budget: Budgets
    Catagories: Catagories
    payment_modes: PaymentModes
    user_details: User

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        self.start = start_date
        self.end = end_date

    def __setattr__(self, name: str, value: object) -> None:
        match name:
            case "start":
                if value.__class__ != date:
                    raise Exception("0xegbl0004")
                
            case "end":
                if value.__class__ != date:
                    raise Exception("0xegbl0004")
                
        return super().__setattr__(name, value)

    def __contains__(self, key: object) -> bool:
        if key.__class__ != date:
            raise Exception("0xegbl0004")
        
        if key >= self.start and key < self.end:
            return True
        
        return False

class DatetimeRange:
    def __init__(self, start_datetime: datetime, end_datetime: datetime):
        self.start = start_datetime
        self.end = end_datetime

    def __setattr__(self, name: str, value: object) -> None:
        match name:
            case "start":
                if value.__class__ != datetime:
                    raise Exception("0xegbl0004")
                
            case "end":
                if value.__class__ != datetime:
                    raise Exception("0xegbl0004")
                
        return super().__setattr__(name, value)
    
    def __contains__(self, key: object) -> bool:
        if key.__class__ != datetime:
            raise Exception("0xegbl0004")
        
        if key >= self.start and key < self.end:
            return True
        
        return False
    
{Transaction(1,1,1,1,1,1,1,1,1)}