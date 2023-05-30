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
    from typing import Any
    from datetime import date, datetime
except:
    raise Exception("0xegbl0001")

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        self.start = start_date
        self.end = end_date

    def __setattr__(self, name: str, value: Any) -> None:
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

    def __setattr__(self, name: str, value: Any) -> None:
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