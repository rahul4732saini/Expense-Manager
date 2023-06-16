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

from sys import path
path.append("..\\Expense Manager")

import re
from dataclasses import dataclass
from datetime import date, datetime

class Transaction:
    def __init__(
            self,
            id: str,
            status: str,
            amount: int | float,
            type: str,
            payment_mode: str,
            date_time: datetime,
            description: str
    ):
        
        self.id = id
        self.status = status
        self.amount = amount
        self.type = type
        self.payment_mode = payment_mode
        self.date_time = date_time
        self.description = description

    def __eq__(self, other: object) -> bool:
        assert other.__class__ == self.__class__

        return self.id == other.id

@dataclass
class Budget:
    budget_id: str
    range: int | float
    month: str
    year: str
    catagories: dict | None
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Budget):
            return False
        
        return self.budget_id == other.budget_id

@dataclass
class Budgets:
    budgets: list[Budget]

@dataclass
class Catagory:
    name: str
    color: str
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Catagory):
            return False
        
        return self.name == other.name

@dataclass
class Catagories:
    income_catagories: list[Catagory]
    expense_catagories: list[Catagory]

@dataclass 
class PaymentMode:
    name: str
    color: str
    catagory: str
    initial_balance: int | float
    
    def __eq__(self, other: object):
        if not isinstance(other, PaymentMode):
            return False
        
        return self.name == other.name

@dataclass
class PaymentModes:
    payment_modes: list[PaymentMode]

@dataclass
class User:
    first_name: str
    middle_name: str
    last_name: str
    email_id: str
    region: str
    date_of_birth: date

@dataclass
class Settings:
    theme: str
    default_payment_mode: str
    currency: str

@dataclass
class AllData:
    budgets: Budgets
    catagories: Catagories
    payment_modes: PaymentModes
    user_details: User

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        self.start = start_date
        self.end = end_date

    def __setattr__(self, name: str, value: object) -> None:
        match name:
            case "start":
                assert value.__class__ != date, "0xegbl0004"
                
            case "end":
                assert value.__class__ == date, "0xegbl0004"
                
        return super().__setattr__(name, value)

    def __contains__(self, key: object) -> bool:
        assert key.__class__ == date, "0xegbl0004"
        
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
                assert value.__class__ == datetime, "0xegbl0004"
                
            case "end":
                assert value.__class__ == datetime, "0xegbl0004"
                
        return super().__setattr__(name, value)
    
    def __contains__(self, key: object) -> bool:
        assert key.__class__ == datetime, "0xegbl0004"
        
        if key >= self.start and key < self.end:
            return True
        
        return False
    
datetime(2023, 5, 23)._year