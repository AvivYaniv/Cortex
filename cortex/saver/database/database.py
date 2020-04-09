import threading

DATABASE_DEFAULT_HOST   =   'localhost'

# TODO : Replace with real code
class _DataBase:
    _shared_state = {}
    
    def __init__(self, logger, host, port):
        self.__dict__   = self.__class__._shared_state
        self.logger     = logger
        self.lock       = threading.Lock()
        self.host       = host if host else DATABASE_DEFAULT_HOST
        self.port       = port
    
    def commit(self, data):
        self.lock.acquire()
        try:
            print(f'Commited : {data}')
        finally:            
            self.lock.release()
            