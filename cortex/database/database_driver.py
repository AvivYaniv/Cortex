
# Constants Section
DATABASE_DEFAULT_HOST       =   'localhost'

class _DataBaseDriver:
    _shared_state = {}
    # Constructor Section
    def __init__(self, logger, host, port):
        self.__dict__   = self.__class__._shared_state
        self.logger     = logger
        self.host       = host if host else DATABASE_DEFAULT_HOST
        self.port       = port
