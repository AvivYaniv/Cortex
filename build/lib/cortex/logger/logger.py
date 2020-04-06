import yaml
import os
import logging.config
from builtins import staticmethod

# Logging configuraition file
LOGGER_CONFIG_FILE_TYPE = '.yaml'
LOGGER_CONFIG_FILE_PATH = 'logger/logging_config.yaml'

# Messages
INFO_LOADING_LOG_CONFIG                         = 'Loading log configuration...'

ERROR_UNKNOWN_TYPE_CONFIGURATION_FILE_NOT_FOUND = 'Error unknown type of logging Configuration. Using default configs'
ERROR_PARSING_CONFIGURATION_FILE_NOT_FOUND      = 'Error in parsing logging Configuration. Using default configs'

def yaml_file_to_dictionary_reader(f):
    dictionary = yaml.safe_load(f.read())
    return dictionary

CONFIG_FILE_READERS = { '.yaml' : yaml_file_to_dictionary_reader }

class _LoggerLoader:
    _shared_state = {}
    
    s_is_log_config_initialized = False
    
    def __init__(self):
        self.__dict__ = self.__class__._shared_state
    
    @staticmethod    
    def read_log_config_to_dictionary(fpath=LOGGER_CONFIG_FILE_PATH):
        _, file_extension = os.path.splitext(fpath)    
        dictionary = None    
        if file_extension not in CONFIG_FILE_READERS:
            print(ERROR_UNKNOWN_TYPE_CONFIGURATION_FILE_NOT_FOUND)
            return dictionary        
        if os.path.exists(fpath):
            with open(fpath, 'rt') as f:
                try:
                    dictionary = CONFIG_FILE_READERS[file_extension](f) 
                except Exception as e:
                    print(ERROR_PARSING_CONFIGURATION_FILE_NOT_FOUND)
        return dictionary 
    
    def load_log_config(self, default_level=logging.INFO):
        if not _LoggerLoader.s_is_log_config_initialized:
            print(INFO_LOADING_LOG_CONFIG)
            config_dictionary = None
            config_dictionary = _LoggerLoader.read_log_config_to_dictionary()
            if config_dictionary:
                logging.config.dictConfig(config_dictionary)
            else: 
                logging.basicConfig(level=default_level)
            _LoggerLoader.s_is_log_config_initialized = True
        