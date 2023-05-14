try:
    from sys import path
    path.append("..\\Expense Manager")

    import data.info as info
    from random import choice
    from os.path import exists
    import data.pre_requisites as pre_requisites
    from typing import Union
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_modes(self) -> list[dict]:
        if exists(info.DATA_PAYMENT_MODES) == False:
            raise Exception("0xepym0001")
        
        # Accessing and Reading the payment modes file and verifying it.
        try:
            with open(info.DATA_PAYMENT_MODES, 'r') as file:
                payment_modes: list = eval(file.read().replace("\n", ""))

            if payment_modes.__class__ != list:
                raise Exception
        except Exception:
            raise Exception("0xepym0002")

        length_limit_exceed: bool = payment_modes.__len__() > 30

        if length_limit_exceed:
            raise Exception("0xepym0011")
        
        # Checking for duplicate dictionaries in the payment modes list.
        if payment_modes.__len__() != [eval(i) for i in set([str(i) for i in payment_modes])].__len__():
            raise Exception("0xepym0012")

        # Verifying each payment mode dictionary in the list of payment modes.
        for index, element in enumerate(payment_modes):
            try:
                self._verify(element)
            except Exception:
                raise Exception("0xepym0002")
            
            current_balance = payment_modes[index]["current_balance"]
            payment_modes[index]["current_balance"] = round(current_balance, 2) if current_balance.__class__ == float else current_balance

        return payment_modes
    
    def get_mode_names(self) -> list[str]:
        return [i.get("name") for i in self.get_modes()]

    def _verify(self, mode: dict) -> None:
        if mode.__class__ != dict:
            raise Exception("0xepym0003")

        # Verfying the keys and values of the payment mode dictionary provided as the argument.
        if all(
            [
                mode.get("name").__class__ == str,
                mode.get("catagory") in pre_requisites.PAYMENT_MODE_CATAGORIES,
                mode.get("current_balance").__class__ in [int, float] and mode.get("current_balance") > 0,
                mode.get("color") in pre_requisites.COLORS
            ]
        ) == False:
            raise Exception("0xepym0003")
        
        if mode.get("name").__len__() > 25:
            raise Exception("0xepym0004")

    def _write_file(self, payment_modes: list, check_last: bool) -> None:
        if check_last == True:
            self._verify(payment_modes[-1])
        
        # Converting the list into a readable string format to be written in the payment modes data file.
        payment_modes = str(payment_modes).replace("{", "{\n").replace("}", "\n}").replace("[", "[\n").replace("]", "\n]").replace(", ", ",\n")

        with open(info.DATA_PAYMENT_MODES, 'w') as file:
            file.write(payment_modes)

    def add_mode(self,
                 name: str,
                 catagory: str,
                 current_balance: Union[int, float] = 0) -> None:
        
        if self.get_modes().__len__() >= 30:
            raise Exception("0xepym0005")

        color = choice(pre_requisites.COLORS)

        entry = {
            "name": name,
            "color": color,
            "current_balance": round(current_balance, 2) if current_balance.__class__ == float else current_balance,
            "catagory": catagory
        }

        payment_modes: list = self.get_modes()
        payment_modes.append(entry)
        self._write_file(payment_modes, check_last = True)

    def delete_mode(self, mode_names: list[str]) -> None:

        # List of payment mode names queued for deletion that exist, i.e., are valid.
        valid_mode_names: list = [i.get("name") for i in self.get_modes() if i.get("name") in mode_names]

        # Checking if all the payment modes queued for deletion exist.
        if valid_mode_names.__len__() == self.get_mode_names().__len__():
            raise Exception("0xepym0006")
        
        payment_modes = [i for i in self.get_modes() if i.get("name") not in valid_mode_names]
        self._write_file(payment_modes, check_last = False)

        if mode_names.__len__() != valid_mode_names.__len__():
            raise Exception("0xepym0007")

    def edit_mode(self,
                  current_name: str,
                  new_name: str = None,
                  current_balance: Union[int ,float] = None,
                  catagory: str = None) -> None:
        name = new_name

        if name in self.get_mode_names():
            raise Exception("0xepym0010")

        edit = {key:value for key, value in locals().items() if key not in ["self", "current_name", "new_name"] and value != None}

        if edit.__len__() == 0:
            raise Exception("0xepym0009")
        
        try:
            i: dict
            for i in self.get_modes():
                if i.get("name") == current_name:
                    content: dict = i
                    break
            else:
                raise Exception
        except Exception:
            raise Exception("0xepym0008")

        if edit.get("current_balance") != None:
            edit["current_balance"] = round(current_balance, 2) if current_balance.__class__ == float else current_balance
        
        payment_modes = [i for i in self.get_modes() if i.get("name") != current_name]
        content.update(edit)
        payment_modes.append(content)

        self._write_file(payment_modes, check_last = True)

class TroubleShoot:
    def er_0xepym0001(self):
        ...

    def er_0xepym0002(self):
        ...