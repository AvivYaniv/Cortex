import os

import logging
from cortex.logger import _LoggerLoader

from cortex.utils import get_project_file_path_by_caller
from cortex.readers.dictionary import DictionayReaderDriver

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Logging configuration file
MESSAGE_QUEUE_CONFIG_FILE_NAME_SUFFIX           = '_config.yaml'

# Messages
INFO_LOADING_MQ_CONFIG                          = 'Loading message queue configuration...'

ERROR_UNKNOWN_TYPE_CONFIGURATION_FILE_NOT_FOUND = 'Error unknown file type of message queue configuration!'
ERROR_PARSING_CONFIGURATION_FILE                = 'Error in parsing message queue configuration'

class _MessageQueueContextLoader:
    _shared_state = {}
    
    s_is_mq_config_initialized = False
    
    def __init__(self, message_queue_type):
        self.__dict__ = self.__class__._shared_state
        self._load_mq_config(message_queue_type)
    
    @staticmethod    
    def get_mq_config_file_name(message_queue_type):
        return message_queue_type + MESSAGE_QUEUE_CONFIG_FILE_NAME_SUFFIX
    
    @staticmethod    
    def read_mq_config_to_dictionary(message_queue_type):
        fname = _MessageQueueContextLoader.get_mq_config_file_name(message_queue_type)
        dictionary = None   
        dictionary_reader_driver = DictionayReaderDriver.find_driver(fname)
        if not dictionary_reader_driver:
            print(ERROR_UNKNOWN_TYPE_CONFIGURATION_FILE_NOT_FOUND)
            return dictionary      
        fpath = get_project_file_path_by_caller(fname)   
        if os.path.exists(fpath):
            with open(fpath, 'rt') as f:
                try:
                    dictionary = dictionary_reader_driver(f) 
                except:
                    print(ERROR_PARSING_CONFIGURATION_FILE)
        return dictionary 
    
    def _load_mq_config(self, message_queue_type):
        if not _MessageQueueContextLoader.s_is_mq_config_initialized:
            logger.info(INFO_LOADING_MQ_CONFIG)
            config_dictionary               = None
            config_dictionary               = _MessageQueueContextLoader.read_mq_config_to_dictionary(message_queue_type)
            if config_dictionary:
                self.config_dictionary = config_dictionary
                _MessageQueueContextLoader.s_is_mq_config_initialized = True
        
    def get_mq_config(self):
        if _MessageQueueContextLoader.s_is_mq_config_initialized:
            return self.config_dictionary
        return None
    