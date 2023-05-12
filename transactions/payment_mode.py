from sys import path
path.append("..\\Expense Manager")

import os.path
import data.info as info
from typing import Union
from random import choice
from transactions.details import manage

class manage:
    def get_modes(self) -> list:
        if os.path.exists(info.DATA_PAYMENT_MODES) == False:
            raise Exception()
        
        try:
            with open(info.DATA_PAYMENT_MODES, 'r') as file:
                payment_modes: dict = eval(file.read().replace("\n", ""))
        except Exception:
            raise Exception()
        
        return payment_modes
    
    def _verify(self) -> None:
        ...

    def _write_file(self) -> None:
        ...

    def add_mode(self) -> None:
        ...

    def delete_mode(self) -> None:
        ...

    def edit_mode(self) -> None:
        ...