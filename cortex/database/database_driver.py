
# Constants Section
DATABASE_DEFAULT_HOST       =   '0.0.0.0'

class _DataBaseDriver:
    IMPLEMENTATION_FILEDS   =   []  # Fields that are part of database implementation, therefore shouldn't be exported
    _shared_state           =   {}    
    # Constructor Section
    def __init__(self, logger, host, port):
        self.__dict__   = self.__class__._shared_state
        self._logger    = logger
        self.host       = host if host else DATABASE_DEFAULT_HOST
        self.port       = port
    
    # Initialization Methods
    def create_tables(self):
        self._logger.info('tables creation has finished!')
        pass
    def create_triggers(self):
        self._logger.info('triggers creation has finished!')
        pass
    def _create(self):
        self.create_tables()
        self.create_triggers()
