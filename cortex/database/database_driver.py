
# Constants Section
DATABASE_DEFAULT_HOST       =   'localhost'

class _DataBaseDriver:
    _shared_state = {}
    # Constructor Section
    def __init__(self, logger, host, port):
        self.__dict__   = self.__class__._shared_state
        self._logger    = logger
        self.host       = host if host else DATABASE_DEFAULT_HOST
        self.port       = port

    # Initialization Methods
    def create_tables(self):
        self._logger('tables creation has finished!')
        pass
    
    def create_triggers(self):
        self._logger('triggers creation has finished!')
        pass
    
    # Core Logic Method
    def run(self):
        self.create_tables()
        self.create_triggers()
