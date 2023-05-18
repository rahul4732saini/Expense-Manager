r"""
Module related to functions for capturing
directory contents.

(Class) Indexer:
----------------
-   get_file: returns a list of all the files in the directory path proivded.
-   get_subdirs: returns a list of all sub-directories in the directory path provided.
"""

from typing import Any
from os import path, listdir

class Indexer:
    def __init__(self,dir_path:str):
        self.dir_path = dir_path

    def __repr__(self):
        return f"dir_path = {self.dir_path}"

    def __setattr__(self, name: str, value: Any):
        if name == "dir_path" and not path.exists(value):
            raise Exception("0xedir0001")
        
        return super().__setattr__(name, value)
    
    def get_files(self) -> list:
        return [i for i in listdir(self.dir_path) if path.isfile("%s\\%s" % (self.dir_path, i))]
    
    def get_subdirs(self) -> list:
        return [i for i in listdir(self.dir_path) if path.isdir("%s\\%s" % (self.dir_path, i))]