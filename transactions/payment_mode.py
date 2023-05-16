r"""
Module related to functions required for the
management and troubleshooting of payment modes.

This exports:

(Class) Manage:
    get_modes: return all the existing payment modes dictionaries.
    get_mode_name: returns all the names of the existing payment modes.
    add_mode: used to add a new payment mode.
    delete_mode: used for deleting payment modes. Takes payment mode names as arguments within a list.
    edit_mode: used for editing a payment mode's details.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    import random
    import os.path
    from typing import Union
    import data.info as info
    import data.troubleshoot as troubleshoot
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_modes(self) -> list[dict]:
        if os.path.exists(info.DATA_PAYMENT_MODES) == False:
            raise Exception("0xepym0001")
        
        # Accessing and Reading the payment modes file and verifying it.
        try:
            with open(info.DATA_PAYMENT_MODES, 'r') as file:
                payment_modes: list[dict] = eval(file.read().replace("\n", ""))

            if payment_modes.__class__ != list:
                raise Exception
            
            mode_names: list[str] = [i.get("name") for i in payment_modes]
        except Exception:
            raise Exception("0xepym0002")
        
        length_limit_exceed: bool = payment_modes.__len__() > 30

        # Checking if the number of payment modes exceed the limit of 30.
        if length_limit_exceed:
            raise Exception("0xepym0011")
        
        # Checking for duplicate payment mode names
        if mode_names.__len__() != set(mode_names).__len__():
            raise Exception("0xepym0012")

        # Verifying each payment mode dictionary in the list of payment modes.
        index: int
        element: dict
        for index, element in enumerate(payment_modes):
            try:
                self._verify(element)
            except Exception:
                raise Exception("0xepym0002")
            
            # Rounding off the current balance value to the nearest 2 decimal places if it is a float value.
            initial_balance = payment_modes[index]["initial_balance"]
            payment_modes[index]["initial_balance"] = round(initial_balance, 2) if initial_balance.__class__ == float else initial_balance

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
                mode.get("initial_balance").__class__ in [int, float] and mode.get("initial_balance") >= 0,
                mode.get("color") in pre_requisites.COLORS
            ]
        ) == False:
            raise Exception("0xepym0003")
        
        if mode.get("name").__len__() > 25:
            raise Exception("0xepym0004")

    def _write_file(self, payment_modes: list[dict]) -> None:
        
        # Converting the list into a readable string format to be written in the payment modes data file.
        payment_modes = str(payment_modes).replace("{", "{\n").replace("}", "\n}").replace("[", "[\n").replace("]", "\n]").replace(", ", ",\n")

        with open(info.DATA_PAYMENT_MODES, 'w') as file:
            file.write(payment_modes)

    def add_mode(self,
                 name: str,
                 catagory: str,
                 initial_balance: Union[int, float] = 0) -> None:
        
        if self.get_modes().__len__() >= 30:
            raise Exception("0xepym0005")

        if name in self.get_mode_names():
            raise Exception("0xepym0010")

        color: str = random.choice(pre_requisites.COLORS)

        entry: dict = {
            "name": name,
            "color": color,
            "initial_balance": round(initial_balance, 2) if initial_balance.__class__ == float else initial_balance,
            "catagory": catagory
        }

        payment_modes: list[dict] = self.get_modes()
        payment_modes.append(entry)

        # Only verifying the last payment mode dictionary as all others are already verified.
        self._verify(payment_modes[-1])
        self._write_file(payment_modes)

    def delete_mode(self, mode_names: Union[str, list[str]]) -> None:
        if mode_names.__class__ not in [list, str]:
            raise Exception("0xepym0013")

        # List of payment mode names queued for deletion that exist, i.e., are valid.
        valid_mode_names: list = [i.get("name") for i in self.get_modes() if i.get("name") in (mode_names if mode_names.__class__ == list else [mode_names])]

        # Checking if all the payment modes queued for deletion exist.
        if valid_mode_names.__len__() == self.get_mode_names().__len__():
            raise Exception("0xepym0006")
        
        # Creating payment modes list of only dictionaries that aren't queued for deletion.
        payment_modes: list[dict] = [i for i in self.get_modes() if i.get("name") not in valid_mode_names]
        self._write_file(payment_modes)

        # Raising error if one or more of the payment modes names provided are not existant.
        if (mode_names if mode_names.__class__ == list else [mode_names]).__len__() != valid_mode_names.__len__():
            raise Exception("0xepym0007")

    def edit_mode(self,
                  current_name: str,
                  new_name: str = None,
                  initial_balance: Union[int ,float] = None,
                  catagory: str = None) -> None:
        name: str = new_name

        if name in self.get_mode_names():
            raise Exception("0xepym0010")

        # Dictionary of the edits to be updated in the payment mode.
        edit: dict = {key:value for key, value in locals().items() if key not in ["self", "current_name", "new_name"] and value != None}

        if edit.__len__() == 0:
            raise Exception("0xepym0009")
        
        # Fetching the dictionary with the name to edited.
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

        if edit.get("initial_balance") != None:\
            # Rounding off the current balance value to the nearest 2 decimal places if it is a float value.
            edit["initial_balance"] = round(initial_balance, 2) if initial_balance.__class__ == float else initial_balance
        
        payment_modes: list[dict] = [i for i in self.get_modes() if i.get("name") != current_name]
        content.update(edit)
        payment_modes.append(content)

        # Only verifying the last payment mode dictionary as all others are already verified.
        # Writing it to the data file thereafter.
        self._verify(payment_modes[-1])
        self._write_file(payment_modes)

class TroubleShoot:
    # The following return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    def er_0xepym0001(self) -> bool:
        if os.path.exists(info.DATA_PAYMENT_MODES):
            return True
        
        with open(info.DATA_PAYMENT_MODES, 'w') as file:
            file.write(troubleshoot.PAYMENT_MODE["0xepym0001"]["data_file_content"])

        return True

    def er_0xepym0002(self):
        ...

    def er_0xepym0011(self):
        ...