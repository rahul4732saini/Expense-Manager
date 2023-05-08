try:    
    from sys import path
    path.append("..\\Expense Manager")

    import os.path
    import data.info as info
    from random import choice
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class income:
    def get_catagories(self, file:str = "income.txt") -> dict:
        if file not in pre_requisites.CATAGORY_FILES:
            raise Exception("0xecat0011")

        if os.path.exists("%s\\%s" % (info.DATA_CATAGORIES, file)) == False:
            if os.path.exists(info.DATA_CATAGORIES) == False:
                raise Exception("0xecat0001")
            elif True:
                raise Exception("0xecat0002") if file == "income.txt" else Exception("0xecat0010")

        try:
            with open("%s\\%s" % (info.DATA_CATAGORIES,file)) as text:
                catagories:dict = eval(text.read().replace("\n",""))

            if catagories.__class__ == dict and all([i in pre_requisites.COLORS for i in catagories.values()]) == False:
                raise Exception
        except:
            raise Exception("0xecat0003") if file == "income.txt" else Exception("0xecat0012")
        
        return catagories

    def _write_catagory(self, catagories_dict:dict, file:str = "income.txt") -> None:
        catagories:list = list(str(catagories_dict).replace(", ", ",\n"))
        catagories.insert(1,"\n")
        catagories.insert(-1,"\n")
        catagories = "".join(catagories)

        with open("%s\\%s" % (info.DATA_CATAGORIES, file),'w') as text:
            text.write(catagories)

    def add_catagory(self, catagory_name:str) -> None:
        if len(catagory_name) == 0 and catagory_name.__class__ != str:
            raise Exception("0xecat0004")
        
        if catagory_name in self.get_catagories().keys():
            raise Exception("0xecat0009")
        
        catagories:dict = self.get_catagories()
        catagories.update({catagory_name:choice(pre_requisites.COLORS)})
        self._write_catagory(catagories, file = "income.txt" if self.__class__.__name__ == "income" else "expense.txt")

    def remove_catagories(self, catagories:list) -> None:
        if catagories.__class__ not in [list,tuple,set]:
            raise Exception("0xecat0007")

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
    def get_catagories(self, file = "expense.txt") -> dict:
        return super().get_catagories(file)

    def add_catagory(self, catagory_name: str) -> None:
        super().add_catagory(catagory_name)
    
    def remove_catagories(self, catagories: list) -> None:
        super().remove_catagories(catagories)
    
    def edit_catagory(self, old_catagroy_name: str, new_catagory_name: str) -> None:
        super().edit_catagory(old_catagroy_name, new_catagory_name)