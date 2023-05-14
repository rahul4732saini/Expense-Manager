try:
    from sys import path
    path.append("..\\Expense Manager")

    import pandas
    import os.path
    from details import manage
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class transactions:
    def __init__(self,
                transactions_id: list[str],
                save_location: str,
                file_name: str):
        self.transactions_id = transactions_id
        self.save_location = save_location
        self.file_name = file_name

        if all([i in manage().get_transactions_id() for i in transactions_id]) == False:
            raise Exception("0xetrn0ex1")
        
        if os.path.exists(self.save_location) == False:
            raise Exception("0xetrn0ex2")
        
        if self.file_name.__len__() == 0:
            raise Exception("0xetrn0ex3")

    def _to_dataframe(self) -> pandas.DataFrame:
        try:
            transactions_details: list = [i for i in manage().read_transactions() if i.get("transaction_id") in self.transactions_id]
        except Exception:
            raise Exception("0xetrn0ex4")
            
        return pandas.DataFrame(transactions_details, columns = pre_requisites.TRANSACTION_KEYS)
    
    def to_csv(self) -> None:
        self._to_dataframe().to_csv("%s\\%s.csv" % (self.save_location, self.file_name), index = False)