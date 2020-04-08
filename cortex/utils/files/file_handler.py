import threading

from pathlib import Path, PurePath

class _FileHandler:
    lock            = threading.Lock()
    _shared_state   = {}
    
    def __init__(self):
        self.__dict__ = self.__class__._shared_state
    
    @staticmethod
    def to_safe_file_path(directory, file):
        return _FileHandler.to_safe_path(str(PurePath(directory) / Path(file)))
    
    @staticmethod
    def to_safe_path(path_name):
        return path_name.replace(':', '-').replace(' ', '_')
            
    def save(self, file_path, data, mode='a+'):
        self.lock.acquire()
        is_written  = False
        try:
            with open(file_path, mode) as file:                             
                file.write(data)
            is_written = True
        finally:            
            self.lock.release()
        return is_written