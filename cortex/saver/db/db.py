import threading

# TODO : Replace with real code
class _DataBase:
    _shared_state = {}
     
    def __init__(self, database_type=None, database_host=None, database_port=None):    
        self.__dict__   = self.__class__._shared_state
        self.lock       = threading.Lock()
    
    def commit(self, data):
        self.lock.acquire()
        try:
            print(f'Commited : {data}')
        finally:            
            self.lock.release()
            