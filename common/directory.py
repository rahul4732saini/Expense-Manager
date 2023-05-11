from os import path, listdir

class indexer:
    def __init__(self,dir_path:str):
        self.dir_path = dir_path

        if path.exists(self.dir_path) == False:
            raise Exception("0xedir0001")

    def get_content(self) -> list:
        return listdir(self.dir_path)
    
    def get_files(self) -> list:
        return [i for i in self.get_content() if path.isfile("%s\\%s" % (self.dir_path, i))]
    
    def get_subdir(self) -> list:
        return [i for i in self.get_content() if path.isdir("%s\\%s" % (self.dir_path, i))]