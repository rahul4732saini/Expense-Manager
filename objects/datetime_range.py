from datetime import date, datetime

# Broken Code...
# To be fixed...

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        self.__start = start_date
        self.__end = end_date

    @property
    def start(self):
        return self.__start
    
    @start.setter
    def start(self, value):
        if value.__class__ != date:
            raise Exception
        
        self.start = value
    
    @property
    def end(self):
        print("property")
        return self.__end
    
    @end.setter
    def end(self, value):
        if value.__class__ != date:
            raise Exception
        
        print("called")
        if value < self.start:
            raise Exception
        
        self.end = value

class DatatimeRange:
    def __init__(self, start_datetime: datetime, end_datetime: datetime):
        self.__start = start_datetime
        self.__end = end_datetime

# pending...