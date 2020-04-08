import os

from cortex.utils import DynamicModuleLoader

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
PARSER_NOT_FOUND_ERROR_MESSAGE  =   'Parser function/class not found in directory'

class Parser:
    LOOKUP_TOKEN        =   'parser'
    NAME_IDENTIFIER     =   'field'
    
    def __init__(self, parser_type):
        self.initialized = True
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        self._function_parsers, self._class_parsers = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        self._set_parser_function(parser_type)
        
    def parse(self, saver, context, snapshot):        
        return self._parser_function(saver, context, snapshot)

    def _set_parser_function(self, parser_type):
        self._parser_object     = None
        self._parser_function   = None
        if parser_type in self._class_parsers.keys():
            self._parser_object     = self._class_parsers[parser_type]()
            self._parser_function   = self._parser_object.parse
        elif parser_type in self._function_parsers.keys():
            self._parser_function   = self._function_parsers[parser_type]
        else:
            logger.error(PARSER_NOT_FOUND_ERROR_MESSAGE)
            self.initialized = False        
            