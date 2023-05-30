r"""
Module used for exporting transactions in the form
of PDF / CSV.

This exports:

(Class) Transactions:
---------------------
-   to_CSV: converts the transactions into a CSV file.
-   to_PDF: converts the transactions provided into a PDF file.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    import pandas
    import os.path
    from details import Manage
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class Transactions:
    def __init__(self,
                transactions_id: list[str],
                save_location: str,
                savefile_name: str):
        
        self.transactions_id = transactions_id
        self.save_location = save_location
        self.savefile_name = savefile_name

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"transactions_id = {self.transactions_id if self.transactions_id.__class__ == list else [self.transactions_id]}",
                f"save_location = {self.save_location}",
                f"savefile_name = {self.savefile_name}"
            )
        )

    def __setattr__(self, name: str, value: object):
        match name:
            case "transactions_id":
                if value.__class__ != list or not all((i in Manage().get_transactions_id() for i in value)):
                    raise Exception("0xetrn0ex1")
            
            case "save_location":
                if not os.path.exists(value):
                    raise Exception("0xetrn0ex2")
                
            case "savefile_name":
                if value.__len__() not in range(1, 50):
                    raise Exception("0xetrn0ex3")
        
        return super().__setattr__(name, value)

    def _to_DataFrame(self) -> pandas.DataFrame:
        try:
            transactions_details: list = [i for i in Manage().get_transactions() if i["transaction_id"] in self.transactions_id]
        except Exception:
            raise Exception("0xetrn0ex4")
            
        return pandas.DataFrame(transactions_details, columns = pre_requisites.TRANSACTION_KEYS)
    
    def to_CSV(self) -> None:
        self._to_DataFrame().to_csv("%s\\%s.csv" % (self.save_location, self.savefile_name), index = False)

    def to_PDF(self) -> None:
        ...