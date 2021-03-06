import os.path

from cortex.readers import MindFileReader

from cortex.utils import Connection

from cortex.protocol import ProtocolMessagesTyeps, Protocol

from cortex.readers.reader_versions import ReaderVersions

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                          =   logging.getLogger(__name__)
logger_loader                   =   _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
DEFAULT_HOST                    =    '127.0.0.1'
DEFAULT_PORT                    =    '8000'
DEFAULT_FILE_PATH               =    'sample.mind.gz'
DEFAULT_FILE_VERSION            =    ReaderVersions.PROTOBUFF

# Messages Section
FILE_NOT_FOUND_MESSAGE_FORMAT   =   'sample file not found at path %s'

# Setting default protocol    
protocol = Protocol() 

class ClientService:
    # Constructor Section
    def __init__(self, host='', port=''):
        """
        Initializes a client service.
    
        :param host: The server host, if empty - default will be selected.
        :param host: The server port, if empty - default will be selected.            
        """
        # Default parameter resolution
        self._total_snapshots_uploaded  = 0
        self.server_ip_str              = host if host else DEFAULT_HOST
        self.server_port_int            = int(port if port else DEFAULT_PORT)
    # Methods Section
    # Output messages
    @staticmethod
    def get_file_not_found_message(file_path):
        """
        Returns formatted file not found message.
    
        :param file_path: The file not found path, to be formatted in message.    
        """
        return FILE_NOT_FOUND_MESSAGE_FORMAT % ( file_path )
    # Message Creation
    @staticmethod
    def create_message(message_type, *args, **kwargs):
        """
        Creates a message, of `client-server protocol <https://github.com/AvivYaniv/Cortex/blob/master/README.md#513-client-server-protocol>`_.
    
        :param message_type: The message type, according to the protocol.
        :param args: Arguments to create message.
        :param kwargs: Key-value arguments to create message.            
        """
        return protocol.get_message(message_type)(*args, **kwargs)
    
    def send_message(self, message_type, *args, **kwargs):
        """
        Sends a message to server.
    
        :param message_type: The message type to send, from `client-server protocol <https://github.com/AvivYaniv/Cortex/blob/master/README.md#513-client-server-protocol>`_ messages.
        :param args: Arguments to create message.
        :param kwargs: Key-value arguments to create message.        
        """
        message = ClientService.create_message(message_type, *args, **kwargs)
        try:
            self.connection.send_message(message.serialize())            
            if ProtocolMessagesTyeps.SNAPSHOT_MESSAGE == message_type:
                self._total_snapshots_uploaded   += 1
        except Exception as e:                
            logger.error(f'error while sending message type {message_type} : {e}')            
            self._is_valid_connection = False            
 
    # Receives configuration message from server
    def receive_message(self, message_type):
        """
        Receives a message from server.
    
        :param message_type: The message type to receive, from `client-server protocol <https://github.com/AvivYaniv/Cortex/blob/master/README.md#513-client-server-protocol>`_ messages.              
        """
        try:
            message_bytes               = self.connection.receive_message()
        except Exception as e:
            logger.error(f'error receiving message type {message_type} : {e}')
            self._is_valid_connection   = False
            return None
        try:
            message                     = protocol.get_message(message_type).read(message_bytes)
        except Exception as e:            
            logger.error(f'error while parsing message type {message_type} : {e}')
            self._is_valid_connection   = False
            return None
        return message
    
    # Uploads a mind file to server    
    def upload_sample(self, file_path='', version=''):
        """
        Uplads a `mind` file to server.
    
        :param file_path: The `mind` file path to be uploaded.
        :param version: The `mind` file `version <https://github.com/AvivYaniv/Cortex/blob/master/README.md#512-mind-file-formats>`_.              
        """
        file_path       = file_path if file_path else DEFAULT_FILE_PATH
        version         = version if version else DEFAULT_FILE_VERSION
        # Logging initialization
        logger.info(f'initializing client to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')
        # Validating sample file exists - else quitting
        if not os.path.isfile(file_path):
            error_message = ClientService.get_file_not_found_message(file_path)
            logger.error(error_message)
            print(error_message)
            return
        # Initializing connection status as valid
        self._is_valid_connection = True        
        # Reading mind file and sending it to server    
        with MindFileReader(file_path, version) as sample_reader:
            with Connection.connect(self.server_ip_str, self.server_port_int) as connection:                    
                self.connection      =      connection
                # Sending hello message
                user_information     =      sample_reader.user_information
                self._user_id        =      user_information.user_id
                self.send_message(ProtocolMessagesTyeps.HELLO_MESSAGE, user_information)
                if not self._is_valid_connection:
                    return
                # Receiving configuration message
                config_message = self.receive_message(ProtocolMessagesTyeps.CONFIG_MESSAGE)
                if not self._is_valid_connection:
                    return
                fields = config_message.fields            
                # Sending snapshot messages
                for snapshot in sample_reader:
                    self.send_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE, snapshot, fields)
                    if not self._is_valid_connection:
                        return
        # Logging client has finished to upload file
        print(f'client has finished to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')

def upload_sample(host='', port='', file_path='', version=''):
    client_service = ClientService(host, port)
    client_service.upload_sample(file_path, version)
