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
    import data.requirements as requirements
except Exception:
    raise Exception("0xegbl0001")

class Transactions:
    def __init__(self,
                transactions_id: list[str],
                save_directory: str,
                savefile_name: str):
        
        self.transactions_id = transactions_id
        self.save_directory = save_directory
        self.savefile_name = savefile_name

    def _verify_transactions_id(self, transactions_id: list[str]):
        if not all((i in Manage().get_transactions_id() for i in transactions_id)):
            raise Exception()
        
    def _verify_save_directory(self, directory: str):
        if directory.__class__ != str or not os.path.exists(directory):
            raise Exception()
        
    def _verify_savefile_name(self, file: str):
        if file.__class__ != str or len(file) not in range(1, 50):
            raise Exception()
        
        if os.path.exists(f"{self.save_directory}\\{file}"):
            raise Exception()
        
    def __setattr__(self, name: str, value: object):

        verify: dict = {
            "transactions_id": self._verify_transactions_id,
            "save_directory": self._verify_save_directory,
            "savefile_name": self._verify_savefile_name
        }

        # Verifying the attribute.
        verify[name](value)

        return super().__setattr__(name, value)

    def _to_DataFrame(self) -> pandas.DataFrame:
        try:
            transactions_details: list = (i for i in Manage().get_transactions() if i["transaction_id"] in self.transactions_id)
        except Exception:
            raise Exception("0xetrn0ex4")
            
        return pandas.DataFrame(transactions_details, columns = requirements.TRANSACTION_KEYS)
    
    def to_CSV(self) -> None:
        self._to_DataFrame().to_csv("%s\\%s.csv" % (self.save_location, self.savefile_name), index = False)

    def to_PDF(self) -> None:
        ...