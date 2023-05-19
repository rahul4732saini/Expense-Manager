try:
    from sys import path
    path.append("..\\Expense Manager")

    from details import Manage
    from typing import Union, Any
    from transactions.catagory import Expense
except Exception:
    raise Exception("0xegbl0001")

class Budgets:
    def __init__(self):
        ...

    def __repr__(self) -> str:
        return f""

    def __setattr__(self, name: str, value: Any):
        ...

    def filter(self) -> list[dict]:
        return list