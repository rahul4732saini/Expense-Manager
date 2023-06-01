try:
    from sys import path
    path.append("..\\Expense Manager")

    ...
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def add(self, key: str) -> None:
        ...

    def change(self, current_key: str, new_key: str) -> None:
        ...

    def remove(self, current_key: str) -> None:
        ...