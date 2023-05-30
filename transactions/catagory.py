r"""
Module related to functions required for the
management and troubleshooting of catagories (income / expense)
used in transactions and budgets.

This exports:

(Class) Income:
---------------
-   get_catagories: returns a dictionary of all the catagory names and their colors.
-   add_catagory: used to create a new catagory.
-   edit_catagory: used to edit the name of the catagory.

(Class) Expense:
----------------
-   ** Subclass of Income **
-   ** Same functions as of Income **
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

class Income:
    @property
    def file(self):
        return self.__class__.__name__.lower()

    def get_catagories(self) -> dict:

        # Checking the existance of the catagories file path.
        if not os.path.exists("%s\\%s.json" % (info.DATA_CATAGORIES, self.file)):
            if not os.path.exists(info.DATA_CATAGORIES):
                raise Exception("0xecat0001")
            else:
                raise Exception("0xecat0002") if self.file == "income" else Exception("0xecat0007")

        # Accessing the catagory file, capturing the contents and Verifying them.
        try:
            with open("%s\\%s.json" % (info.DATA_CATAGORIES, self.file), 'r') as file:
                catagories: dict = json.load(file)

            if catagories.__class__ != dict:
                raise Exception
            
            if "others" not in catagories:
                raise Exception
        except:
            raise Exception("0xecat0003") if self.file == "income" else Exception("0xecat0008")

        if catagories.__len__() > 50:
            raise Exception("0xecat0009") if self.file == "income" else Exception("0xecat0010")

        # Verifying the catagory file details.
        if not all((key.__class__ == str and value in pre_requisites.COLORS and len(key) <= 25 for key, value in catagories.items())):
            raise Exception("0xecat0003")
        
        return catagories

    def _write_catagory(self, catagories: dict) -> None:
        with open("%s\\%s.json" % (info.DATA_CATAGORIES, self.file), 'w') as file:
            json.dump(catagories, file, indent = 4)

    def _verify_catagory_name(self, catagory_name: str) -> None:
        if catagory_name.__class__ != str or len(catagory_name) == 0:
            raise Exception("0xecat0004")
        
        if len(catagory_name) > 25:
            raise Exception("0xecat0011")
        
        # Checking if the provided argument is already present in the catagory names
        if catagory_name in self.get_catagories().keys():
            raise Exception("0xecat0006")

    def add_catagory(self, catagory_name: str) -> None:
        self._verify_catagory_name(catagory_name)
        
        catagories: dict = self.get_catagories()

        # The new catagory is updated into the catagories dictionary and saved into the catagories file.
        catagories.update({catagory_name: random.choice(pre_requisites.COLORS)})
        self._write_catagory(catagories)

    def edit_catagory(self, old_catagory_name:str, new_catagory_name:str) -> None:
        if old_catagory_name not in self.get_catagories().keys():
            raise Exception("0xecat0005")
        
        self._verify_catagory_name(new_catagory_name)
        
        # Capturing the key value pair with the old_catagory_name.
        catagories:dict = self.get_catagories()
        catagory_color:str = catagories.get(old_catagory_name)

        # Removing the old catagory, adding the new edited one and saving it to the catagories file.
        catagories.pop(old_catagory_name)
        catagories.update({new_catagory_name: catagory_color})
        self._write_catagory(catagories)

class Expense(Income):
    def get_catagories(self) -> dict:
        return super().get_catagories()

    def add_catagory(self, catagory_name: str) -> None:
        super().add_catagory(catagory_name)
    
    def edit_catagory(self, old_catagroy_name: str, new_catagory_name: str) -> None:
        super().edit_catagory(old_catagroy_name, new_catagory_name)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    # To be continued...
    ...