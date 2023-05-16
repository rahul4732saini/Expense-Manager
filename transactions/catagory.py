try:    
    from sys import path
    path.append("..\\Expense Manager")

    import random
    import os.path
    import data.info as info
    from typing import Union
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class income:
    def __init__(self):
        self.file = self.__class__.__name__

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
            raise Exception("0xecat0003") if self.file == "income" else Exception("0xecat0012")

        if catagories.__len__() > 50:
            raise Exception("0xecat0013") if self.file == "income" else Exception("0xecat0014")

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

    def remove_catagories(self, catagories: Union[list[str], str]) -> None:
        if catagories.__class__ not in [list, str]:
            raise Exception("0xecat0007")
        
        catagories = catagories if catagories.__class__ == list else [catagories]

        if all([i in list(self.get_catagories().keys()) for i in catagories]) == False:
            raise Exception("0xecat0005")
        
        if len(catagories) == len(self.get_catagories().keys()):
            raise Exception("0xecat0006")
        
        catagories:dict = {i:j for i,j in self.get_catagories().items() if i not in catagories}
        self._write_catagory(catagories)

    def edit_catagory(self, old_catagroy_name:str, new_catagory_name:str) -> None:
        if old_catagroy_name not in self.get_catagories().keys():
            raise Exception("0xecat0008")
        
        if new_catagory_name in self.get_catagories().keys():
            raise Exception("0xecat0009")

        if new_catagory_name.__len__() == 0 and new_catagory_name.__class__ != str:
            raise Exception("0xecat0004")
        
        catagories:dict = self.get_catagories()
        catagory_color:str = catagories.get(old_catagroy_name)

        catagories.pop(old_catagroy_name)
        catagories.update({new_catagory_name:catagory_color})
        self._write_catagory(catagories)

class expense(income):
    def __init__(self):
        super().__init__()

    def get_catagories(self) -> dict:
        return super().get_catagories()

    def add_catagory(self, catagory_name: str) -> None:
        super().add_catagory(catagory_name)
    
    def remove_catagories(self, catagories: list) -> None:
        super().remove_catagories(catagories)
    
    def edit_catagory(self, old_catagroy_name: str, new_catagory_name: str) -> None:
        super().edit_catagory(old_catagroy_name, new_catagory_name)