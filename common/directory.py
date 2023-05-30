r"""
Module related to functions for capturing
directory contents.

(Class) Indexer:
----------------
-   get_file: returns a list of all the files in the directory path proivded.
-   get_subdirs: returns a list of all sub-directories in the directory path provided.
"""

import os

class Indexer:
    def __init__(self,dir_path:str):
        self.dir_path = dir_path

    def __repr__(self):
        return f"dir_path = {self.dir_path}"

    def __setattr__(self, name: str, value: object):
        if name == "dir_path" and not os.path.exists(value):
            raise Exception("0xedir0001")
        
        return super().__setattr__(name, value)
    
    def get_files(self) -> list[str]:
        return [i for i in os.listdir(self.dir_path) if os.path.isfile("%s\\%s" % (self.dir_path, i))]
    
    def get_subdirs(self) -> list[str]:
        return [i for i in os.listdir(self.dir_path) if os.path.isdir("%s\\%s" % (self.dir_path, i))]