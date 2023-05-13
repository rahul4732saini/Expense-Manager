from os import path, listdir

class indexer:
    def __init__(self,dir_path:str):
        if path.exists(dir_path) == False:
            raise Exception("0xedir0001")

        self.dir_path = dir_path
    
    def get_files(self) -> list:
        return [i for i in listdir(self.dir_path) if path.isfile("%s\\%s" % (self.dir_path, i))]
    
    def get_subdir(self) -> list:
        return [i for i in listdir(self.dir_path) if path.isdir("%s\\%s" % (self.dir_path, i))]