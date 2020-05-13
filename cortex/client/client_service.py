import os.path

from cortex.readers import MindFileReader

from cortex.utils import Connection

from cortex.protocol import ProtocolMessagesTyeps, Protocol

from cortex.readers.reader_versions import ReaderVersions

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
DEFAULT_HOST            =    '127.0.0.1'
DEFAULT_PORT            =    '8000'
DEFAULT_FILE_PATH        =    'sample.mind.gz'
DEFAULT_FILE_VERSION    =    ReaderVersions.PROTOBUFF

# Setting default protocol    
protocol = Protocol() 

class ClientService:
    # Constructor Section
    def __init__(self, host='', port=''):
        """Sends to the server user's sample file"""
        # Default parameter resolution
        self.total_snapshots_uploaded   = 0
        self.server_ip_str              = host if host else DEFAULT_HOST
        self.server_port_int            = int(port if port else DEFAULT_PORT)
    # Methods Section
    # Sends hello message to server
    def send_hello_message(self, user_information):
        hello_message = protocol.get_message(ProtocolMessagesTyeps.HELLO_MESSAGE)(user_information)
        try:
            self.connection.send_message(hello_message.serialize())
        except Exception as e:
            logger.error(f'error while sending hello_message: {e}')            
            self._is_valid_connection = False
            return
    # Receives configuration message from server
    def receive_config_message(self):
        try:
            config_message_bytes           = self.connection.receive_message()
        except Exception as e:
            logger.error(f'error receiving config_message : {e}')
            self._is_valid_connection   = False
            return None
        try:
            config_message                 = protocol.get_message(ProtocolMessagesTyeps.CONFIG_MESSAGE).read(config_message_bytes)
        except Exception as e:
            logger.error(f'error while parsing config_message: {e}')
            self._is_valid_connection     = False
            return None
        return config_message
    # Sends snapshot message to server
    def send_snapshot_message(self, snapshot, fields):
        snapshot_message = protocol.get_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE)(snapshot, fields)
        try:
            self.connection.send_message(snapshot_message.serialize())
            self.total_snapshots_uploaded   += 1
        except Exception as e:
            logger.error(f'error while sending snapshot_message: {e}')
            self._is_valid_connection = False
            return
    # Uploads a mind file to server    
    def upload_sample(self, file_path='', version=''):
        file_path     = file_path if file_path else DEFAULT_FILE_PATH
        version     = version if version else DEFAULT_FILE_VERSION
        # Logging initialization
        logger.info(f'initializing client to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')
        # Validating sample file exists - else quitting
        if not os.path.isfile(file_path):
            logger.error(f'sample file not found at path {file_path}')
            return
        # Initializing connection status as valid
        self._is_valid_connection = True        
        # Reading mind file and sending it to server    
        with MindFileReader(file_path, version) as sample_reader:
            with Connection.connect(self.server_ip_str, self.server_port_int) as connection:                    
                self.connection      =      connection
                # Sending hello message
                user_information     =      sample_reader.user_information                
                self.send_hello_message(user_information)
                if not self._is_valid_connection:
                    return
                # Receiving configuration message
                config_message = self.receive_config_message()
                if not self._is_valid_connection:
                    return
                fields = config_message.fields            
                # Sending snapshot messages
                for snapshot in sample_reader:                    
                    self.send_snapshot_message(snapshot, fields)
                    if not self._is_valid_connection:
                        return
        # Logging client has finished to upload file
        print(f'client has finished to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')

def upload_sample(host='', port='', file_path='', version=''):
    client_service = ClientService(host, port)
    client_service.upload_sample(file_path, version)
