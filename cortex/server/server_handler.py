from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

from cortex.protocol import ProtocolMessagesTyeps, Protocol
from cortex.utils import _FileHandler
from cortex.utils import generate_uuid

from cortex.utils import ConstantPathes

import threading

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                      = logging.getLogger(__name__)
logger_loader               = _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
SNAPSHOT_FILE_NAME          = 'snapshot'

# Supported fields
DEFAULT_SUPPORTED_FIELDS    = [ 'color_image', 'depth_image', 'user_feeling', 'translation', 'rotation' ]

class UserContext:
    def __init__(self, user_info):
        self.user_info = user_info

class ServerHandler(threading.Thread):        
    # Constructor Section
    def __init__(self, connection, publish_snapshot_function):    
        super().__init__()
        self._is_valid_connection       = True
        # Network
        self.connection                 = connection    
        self.files_handler              = _FileHandler()
        # Protocol
        self.supported_fields           = DEFAULT_SUPPORTED_FIELDS
        self.protocol                   = Protocol()
        # Messages
        self.messages                   = MessageQueueMessages()
        # Publish functions
        self.publish_snapshot_function  = publish_snapshot_function
    # Methods Section
    # Protocol Methods Section   
    # Receives hello message from client
    def receive_hello_message(self):
        try:
            hello_message_bytes         = self.connection.receive_message()
        except Exception as e:
            logger.error(f'error receiving hello_message : {e}')
            self._is_valid_connection   = False
            return None
        try:
            hello_message               = self.protocol.get_message(ProtocolMessagesTyeps.HELLO_MESSAGE).read(hello_message_bytes)
        except Exception as e:
            logger.error(f'error parsing hello_message : {e}')
            self._is_valid_connection   = False
            return None
        return hello_message
    # Sends configuration message to client    
    def send_config_message(self):
        config_message                  = self.protocol.get_message(ProtocolMessagesTyeps.CONFIG_MESSAGE)(self.supported_fields)
        try:
            self.connection.send_message(config_message.serialize())
        except Exception as e:
            logger.error(f'error sending config_message to user {self.context.user_info.user_id}: {e}')
            self._is_valid_connection   = False
            return
    # Receives snapshot message from client
    def receive_snapshot_message_bytes(self):
        try:
            snapshot_message_bytes      =   self.connection.receive_message()
        except Exception as e:
            logger.error(f'error receiving snapshot_message of user {self.context.user_info.user_id}: {e}')
            self._is_valid_connection   = False
            return b''
        return snapshot_message_bytes
    # UUID Methods Section
    def _get_uuid(self):
        return generate_uuid()
    # File Handling Methods Section
    # Generate path to save file
    def _get_save_path(self, *pathsegments):
        pathsegments = [str(s) for s in pathsegments]
        return self.files_handler.to_safe_file_path(*pathsegments)
    # Save file
    def _save_file(self, path, data):
        return self.files_handler.save(path, data)
    # Messages Handling Methods Section
    # Sets context
    def _set_context(self, hello_message):
        try:
            self.context            = UserContext(hello_message.user_info)            
        except Exception as e:
            logger.error(f'error parsing hello_message : {e}')
            self._is_valid_connection = False
    def _save_user_info(self):
        user_info_path   =                              \
            self._get_save_path(                        \
                ConstantPathes.DATA_DIRRECTORY,         \
                ConstantPathes.USERS_DIRRECTORY,        \
                self.context.user_info.user_id)
        # Save snapshot
        is_saved         = self._save_file(user_info_path, self.context.user_info.serialize())
        if not is_saved:
            logger.error(f'error saving user info of user {self.context.user_info.user_id}')
            return None
        return user_info_path
    # Saves snapshot
    def _save_snapshot(self, snapshot_uuid, snapshot_message_bytes):
        snapshot_path   =                               \
            self._get_save_path(                        \
                ConstantPathes.DATA_DIRRECTORY,         \
                ConstantPathes.SNAPSHOTS_DIRRECTORY,    \
                self.context.user_info.user_id,         \
                snapshot_uuid,                          \
                SNAPSHOT_FILE_NAME)
        # Save snapshot
        is_saved        = self._save_file(snapshot_path, snapshot_message_bytes)
        if not is_saved:
            logger.error(f'error saving snapshot of user {self.context.user_info.user_id}')
            return None
        return snapshot_path
    # Publish snapshot message
    def publish_snapshot_message(self, snapshot_uuid, raw_snapshot_path):
        # Creating raw snapshot message
        raw_snapshot_message =                                      \
            self.messages.get_message(                              \
                MessageQueueMessagesTyeps.RAW_SNAPSHOT_MESSAGE)(    \
                    self.context.user_info.user_id,                 \
                    snapshot_uuid,                                  \
                    raw_snapshot_path)
        # Publish raw snapshot message
        self.publish_snapshot_function(raw_snapshot_message.serialize())
    # Handle snapshot message
    def handle_snapshot_message(self, snapshot_message_bytes):
        # Gets snapshot uuid
        snapshot_uuid       = self._get_uuid()
        # Saving snapshot
        raw_snapshot_path   = self._save_snapshot(snapshot_uuid, snapshot_message_bytes)
        # If error occurred while saving snapshot
        if not raw_snapshot_path:
            return
        # Publishing snapshot message
        self.publish_snapshot_message(snapshot_uuid, raw_snapshot_path)        
    # Core Logic Methods Section  
    # Runs client handling loop
    def run(self):    
        # Receives hello_message from client
        hello_message = self.receive_hello_message()
        if not self._is_valid_connection:
            return
        # Sets client context based on hello message
        self._set_context(hello_message)        
        # Saving user information
        self._save_user_info() 
        if not self._is_valid_connection:
            return       
        # Sends configuration message to client
        self.send_config_message()
        if not self._is_valid_connection:
            return
        logger.info(f'start receiving snapshots from user {self.context.user_info.user_id}')
        # As long as connection is valid
        while self._is_valid_connection:
            try:
                # Receives snapshot_message from client
                snapshot_message_bytes = self.receive_snapshot_message_bytes()                
                # Handle snapshot message
                self.handle_snapshot_message(snapshot_message_bytes)
            except EOFError:   
                logger.info(f'finished snapshots from user {self.context.user_info.user_id}')         
                break
            # TODO DEBUG RESTORE
            #except Exception as e:
            #    logger.error(f'exception has occurred handling user {self.context.user_info.user_id}: {e}')
