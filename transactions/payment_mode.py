try:
    from sys import path
    path.append("..\\Expense Manager")

    import random
    import os.path
    import data.info as info
    import data.pre_requisites as pre_requisites
    from typing import Union
    from transactions.details import manage
except Exception:
    raise Exception("0xegbl0001")

class manage:
    def get_modes(self) -> list:
        if os.path.exists(info.DATA_PAYMENT_MODES) == False:
            raise Exception()
        
        try:
            with open(info.DATA_PAYMENT_MODES, 'r') as file:
                payment_modes: dict = eval(file.read().replace("\n", ""))
        except Exception:
            raise Exception()
        
        payment_modes = payment_modes[:30] if payment_modes.__len__() > 30 else payment_modes

        for i in payment_modes:
            self._verify(i)
        
        return payment_modes
    
    def get_mode_names(self) -> list:
        return [i.get("name") for i in self.get_modes()]

    def _verify(self, payment_modes: dict) -> None:
        modes = payment_modes

        if all(
            [
                modes.get("name").__class__ == str,
                modes.get("catagory") in pre_requisites.PAYMENT_MODE_CATAGORIES,
                payment_modes.get("current_balance").__class__ in [int, float] and modes.get("current_balance") > 0,
                modes.get("color") in pre_requisites.COLORS
            ]
        ) == False:
            raise Exception()
        
        if modes.get("name").__len__() > 25:
            raise Exception()

    def _write_file(self, entry: list) -> None:
        for i in entry:
            self._verify(i)

        payment_modes: list = self.get_modes()
        payment_modes.append(entry)
        
        payment_modes = str(payment_modes).replace("{", "{\n").replace("}", "\n}").replace("[", "[\n").replace("]", "\n]").replace(", ", ",\n")

        with open(info.DATA_PAYMENT_MODES, 'w') as file:
            file.write(payment_modes)

    def add_mode(self,
                 name: str,
                 catagory: str,
                 current_balance: Union[int, float] = 0) -> None:
        
        color = random.choice(pre_requisites.COLORS)

        entry = {
            "name": name,
            "color": color,
            "current_balance": current_balance,
            "catagory": catagory
        }

        self._write_file([entry])

    def delete_mode(self, mode_name: str) -> None:
        if mode_name not in self.get_mode_names():
            raise Exception()

        payment_modes = [i for i in self.get_modes() if i.get("name") != mode_name]
        self._write_file(payment_modes)

    def edit_mode(self) -> None:
        ...

manage().delete_mode("UPI")