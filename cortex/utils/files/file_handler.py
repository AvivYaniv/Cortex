import os

import threading

import pathlib
from pathlib import Path
from pathlib import PurePath

from cortex.utils.folder import create_files_folder_path

class _FileHandler:
    _lock           = threading.Lock()
    _shared_state   = {}
    
    def __init__(self):
        self.__dict__ = self.__class__._shared_state
        
    @staticmethod
    def to_safe_absolute_file_path(*pathsegments, fname=None, extension=None):
        current_directory = str(pathlib.Path().absolute())
        pathsegments = (current_directory,) + pathsegments
        return _FileHandler.to_safe_file_path(*pathsegments, fname=fname, extension=extension)
    
    @staticmethod
    def to_safe_file_path(*pathsegments, fname=None, extension=None):
        fname = str(fname) if fname else ''
        extension = str(extension) if extension else ''
        pathsegments = [str(s) for s in pathsegments] + [fname + extension]
        full_path = str(PurePath(*pathsegments))
        return _FileHandler.to_safe_path(full_path)
    
    @staticmethod
    def to_safe_path(path_name):
        return path_name.replace(':', '-').replace(' ', '_')
          
    @staticmethod      
    def read_file(file_path, mode=None):
        mode = mode if mode else 'r'
        with open(file_path, mode) as f:
            content = f.read() 
        return content
    
    @staticmethod
    def safe_read_file(file_path, mode=None):
        try:        
            return ( True, _FileHandler.read_file(file_path, mode) )
        except Exception as e:
            return (False, f'Error reading file {file_path} : {e}' )
       
    @staticmethod
    def create_path(path):
        directories = os.path.dirname(path)
        if not os.path.isdir(directories):
            os.makedirs(directories)
            
    def is_file_exists(self, file_path):
        plFilePath = Path(file_path)
        return plFilePath.is_file()        

    def save(self, file_path, data, mode = None):
        is_written  = False
        if not data:            
            return is_written
        create_files_folder_path(file_path)
        self._lock.acquire()
        try:
            _FileHandler.create_path(file_path)
            mode = mode if mode else ('w' if isinstance(data, str) else 'wb')
            with open(file_path, mode) as file:
                file.write(data)
            is_written = True  
        except Exception as e:
            print(f'error saving file {file_path} : {e}')      
        finally:            
            self._lock.release()
        return is_written
    