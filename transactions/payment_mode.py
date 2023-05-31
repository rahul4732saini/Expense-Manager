r"""
Module related to functions required for the
management and troubleshooting of payment modes.

This exports:

(Class) Manage:
---------------
-   get_modes: return all the existing payment modes dictionaries.
-   get_mode_name: returns all the names of the existing payment modes.
-   add_mode: used to add a new payment mode.
-   edit_mode: used for editing a payment mode's details.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    import json
    import random
    import os.path
    import data.info as info
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_modes(self) -> list[dict]:

        # Checking for the existance of the payment modes file.
        if not os.path.exists(info.DATA_PAYMENT_MODES):
                raise Exception("0xepym0001")
        
        # Accessing and Reading the payment modes file and verifying it.
        try:
            with open(info.DATA_PAYMENT_MODES, 'r') as file:
                payment_modes: list[dict] = json.load(file)

            if payment_modes.__class__ != list:
                raise Exception
            
            mode_names: list[str] = [i["name"] for i in payment_modes]
        except Exception:
            raise Exception("0xepym0002")

        if len(payment_modes) > 30:
            raise Exception("0xepym0009")
        
        # Checking for duplicate payment mode names
        if len(mode_names) != len(set(mode_names)):
            raise Exception("0xepym0010")

        # Verifying each payment mode dictionary in the list of payment modes.
        i: dict
        for i  in payment_modes:
            try:
                self._verify(i)
            except Exception:
                raise Exception("0xepym0002")
            
            # Rounding off the current balance value to the nearest 2 decimal places if it is a float value.
            i["initial_balance"] = round(i["initial_balance"], 2)

        return payment_modes
    
    def get_mode_names(self) -> list[str]:
        return [i["name"] for i in self.get_modes()]

    def _verify(self, mode: dict) -> None:
        if mode.__class__ != dict:
            raise Exception("0xepym0003")

        # Verfying the keys and values of the payment mode dictionary provided as the argument.
        try:
            if not all(
                [
                    mode["name"].__class__ == str,
                    mode["color"] in pre_requisites.COLORS,
                    mode["catagory"] in pre_requisites.PAYMENT_MODE_CATAGORIES,
                    mode["initial_balance"].__class__ in (int, float) and mode["initial_balance"] >= 0
                ]
            ):
                raise Exception
        except Exception:
            raise Exception("0xepym0003")
        
        if len(mode["name"]) > 30:
            raise Exception("0xepym0004")

    def _write_mode(self, payment_modes: list[dict]) -> None:
        with open(info.DATA_PAYMENT_MODES, 'w') as file:
            json.dump(payment_modes, file, indent = 4)

    def add_mode(self,
                 name: str,
                 catagory: str,
                 initial_balance: int | float = 0) -> None:
        
        payment_modes = self.get_modes()

        if len(payment_modes) == 30:
            raise Exception("0xepym0005")

        if name in [i["name"] for i in payment_modes]:
            raise Exception("0xepym0008")

        entry: dict = {
            "name": name,
            "color": random.choice(pre_requisites.COLORS),
            "catagory": catagory,
            "initial_balance": round(initial_balance, 2)
        }

        # Verifying the credentials.
        self._verify(entry)

        # Appending the list with the new payment mode.
        payment_modes.append(entry)

        # Writing the edit made to the payment modes file.
        self._write_mode(payment_modes)

    def edit_mode(self,
                  current_name: str,
                  new_name: str = None,
                  initial_balance: int | float = None,
                  catagory: str = None) -> None:
        
        # taking new_name as namespace name.
        name: str = new_name

        payment_modes = self.get_modes()

        if name in [i["name"] for i in payment_modes]:
            raise Exception("0xepym0008")

        # Dictionary of the edits to be updated in the payment mode.
        edit: dict = {key:value for key, value in locals().items() if key not in ["self", "current_name", "new_name", "payment_modes"] and value != None}

        if len(edit) == 0:
            raise Exception("0xepym0007")
        
        # Capturing the dictionary with the name to edited.
        try:
            i: dict
            for i in payment_modes:
                if i["name"] == current_name:
                    content: dict = i
                    break
            else:
                raise Exception
        except Exception:
            raise Exception("0xepym0006")

        if edit.get("initial_balance"):
            # Rounding off the current balance value to the nearest 2 decimal places if it is a float value.
            edit["initial_balance"] = round(initial_balance, 2)
        
        # Removing the existing payment mode and adding the new edited one.
        payment_modes: list[dict] = [i for i in payment_modes if i["name"] != current_name]
        content.update(edit)
        payment_modes.append(content)

        # Only verifying the last payment mode dictionary.
        # Writing it to the data file thereafter.

        self._verify(content)
        self._write_mode(payment_modes)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    def er_0xepym0001(self) -> bool:
        ...

    def er_0xepym0002(self) -> bool:
        ...

    def er_0xepym0009(self) -> bool:
        ...

    def er_0xepym0010(self) -> bool:
        ...

    # To be continued...