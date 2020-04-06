import os
import logging.config

from cortex.utils import get_project_file_path_by_caller
from cortex.readers.dictionary import DictionayReaderDriver

# Logging configuration file
LOGGER_CONFIG_FILE_NAME                         = 'logging_config.yaml'

# Messages
INFO_LOADING_LOG_CONFIG                         = 'Loading log configuration...'

ERROR_UNKNOWN_TYPE_CONFIGURATION_FILE_NOT_FOUND = 'Error unknown file type of logging configuration. Using default configs'
ERROR_PARSING_CONFIGURATION_FILE                = 'Error in parsing logging configuration. Using default configs'

# Constants Section
DEFAULT_LOGGING_LEVEL                           = logging.INFO

class _LoggerLoader:
    _shared_state = {}
    
    s_is_log_config_initialized = False
    
    def __init__(self):
        self.__dict__ = self.__class__._shared_state
    
    @staticmethod    
    def read_log_config_to_dictionary(fname=LOGGER_CONFIG_FILE_NAME):
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
    
    def load_log_config(self, default_level=None):
        default_level = default_level if default_level else DEFAULT_LOGGING_LEVEL
        if not _LoggerLoader.s_is_log_config_initialized:
            print(INFO_LOADING_LOG_CONFIG)
            config_dictionary = None
            config_dictionary = _LoggerLoader.read_log_config_to_dictionary()
            if config_dictionary:
                logging.config.dictConfig(config_dictionary)
            else: 
                logging.basicConfig(level=default_level)
            _LoggerLoader.s_is_log_config_initialized = True
        