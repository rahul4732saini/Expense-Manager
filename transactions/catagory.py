r"""
Module related to functions required for the
management and troubleshooting of catagories (income / expense)
used in transactions and budgets.

This exports:

(Class) Income:
---------------
-   get_catagories: returns a dictionary of all the catagory names and their colors.
-   add_catagory: used to create a new catagory.
-   remove_catagory: used to remove the catagories corresponding to the catagory name(s) provided as str / list.
-   edit_catagory: used to edit the name of the catagory.

(Class) Expense:
----------------
-   ** Subclass of Income **.
-   ** Same functions as of Income **
"""

try:    
    from sys import path
    path.append("..\\Expense Manager")

    import random
    import os.path
    import data.info as info
    from typing import Union, Any
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class Income:
    def __init__(self):
        self.file = self.__class__.__name__.lower()

    def __repr__(self) -> str:
        return f"file = {self.file}"

    def __setattr__(self, name: str, value: Any):

        # Raising an error if the name of the file to be accessed is altered.
        if name == "file" and value != self.__class__.__name__.lower():
            raise Exception("0xegbl0003")
        
        return super().__setattr__(name, value)

    def get_catagories(self) -> dict:

        # Checking the existance of the catagories file path.
        if not os.path.exists("%s\\%s.txt" % (info.DATA_CATAGORIES, self.file)):
            if not os.path.exists(info.DATA_CATAGORIES):
                raise Exception("0xecat0001")
            else:
                raise Exception("0xecat0002") if self.file == "income" else Exception("0xecat0010")

        # Accessing the catagory file, capturing the contents and Verifying them.
        try:
            with open("%s\\%s.txt" % (info.DATA_CATAGORIES, self.file), 'r') as file:
                catagories: dict = eval(file.read().replace("\n",""))

            if catagories.__class__ != dict:
                raise Exception
        except:
            raise Exception("0xecat0003") if self.file == "income" else Exception("0xecat0011")

        if catagories.__len__() > 50:
            raise Exception("0xecat0012") if self.file == "income" else Exception("0xecat0013")

        # Verifying the catagory file details.
        if not all([key.__class__ == str and value in pre_requisites.COLORS for key, value in catagories.items()]):
            raise Exception("0xecat0003")
        
        return catagories

    def _write_catagory(self, catagories_dict: dict) -> None:

        # Converting the dictionary into a readable string format to be written in the catagories (income / expense) data file.
        catagories: str = str(catagories_dict).replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}")

        with open("%s\\%s.txt" % (info.DATA_CATAGORIES, self.file), 'w') as file:
            file.write(catagories)

    def add_catagory(self, catagory_name: str) -> None:
        if len(catagory_name) == 0 or catagory_name.__class__ != str:
            raise Exception("0xecat0004")

        # Checking if the provided argument is already present in the catagory names
        if catagory_name in self.get_catagories().keys():
            raise Exception("0xecat0009")
        
        catagories: dict = self.get_catagories()

        # The new catagory is updated into the catagories dictionary and saved into the catagories file.
        catagories.update({catagory_name: random.choice(pre_requisites.COLORS)})
        self._write_catagory(catagories)

    def remove_catagory(self, catagories: Union[str, list[str]]) -> None:
        if catagories.__class__ not in [list, str]:
            raise Exception("0xecat0007")
        
        catagories = catagories if catagories.__class__ == list else [catagories]

        # List of catagory names that exist, i.e, are valid.
        valid_catagories: list[str] = [i for i in catagories if i in self.get_catagories().keys()]
        
        # Raising error if prompted to remove all catagories.
        if len(valid_catagories) == len(self.get_catagories().keys()):
            raise Exception("0xecat0006")
        
        # Updating the dictionary with catagories not present in the valid catagories and saving it to the catagories file.
        target: dict = {key: value for key, value in self.get_catagories().items() if key not in valid_catagories}
        self._write_catagory(target)

        # Raising an error if invalid catagory names were provided as arguments.
        if len(catagories) != len(valid_catagories):
            raise Exception("0xecat0005")

    def edit_catagory(self, old_catagroy_name:str, new_catagory_name:str) -> None:
        if old_catagroy_name not in self.get_catagories().keys():
            raise Exception("0xecat0008")
        
        if new_catagory_name in self.get_catagories().keys():
            raise Exception("0xecat0009")

        if new_catagory_name.__len__() == 0 and new_catagory_name.__class__ != str:
            raise Exception("0xecat0004")
        
        catagories:dict = self.get_catagories()
        catagory_color:str = catagories.get(old_catagroy_name)

        # Removing the old catagory, adding the new edited one and saving it to the catagories file.
        catagories.pop(old_catagroy_name)
        catagories.update({new_catagory_name: catagory_color})
        self._write_catagory(catagories)

class Expense(Income):
    def __init__(self):
        super().__init__()

    def get_catagories(self) -> dict:
        return super().get_catagories()

    def add_catagory(self, catagory_name: str) -> None:
        super().add_catagory(catagory_name)
    
    def remove_catagory(self, catagories: Union[str, list[str]]) -> None:
        super().remove_catagory(catagories)
    
    def edit_catagory(self, old_catagroy_name: str, new_catagory_name: str) -> None:
        super().edit_catagory(old_catagroy_name, new_catagory_name)

class TroubleShoot:
    # The following return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    # To be continued...
    ...