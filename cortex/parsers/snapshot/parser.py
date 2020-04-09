import os

from cortex.utils import DynamicModuleLoader

from cortex.parsers.snapshot.parser_saver import ParserSaver

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
        self.initialized    = True
        self._saver         = ParserSaver()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        self._function_parsers, self._class_parsers = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        self._set_parser_function(parser_type)
      
    def parse(self, snapshot):
        return self._parser_function(snapshot)
    
    def save_parsed(self, context, result):
        file_path = self._saver.get_path(context, self._parser_extension)
        self._saver.save_file(file_path, result)
        return file_path
        
    def export_parse(self, context, snapshot):   
        result      = self.parse(snapshot)
        if self._is_save_required:
            result = self.save_parsed(context, result)
        return result

    def _set_parser_function(self, parser_type):
        self._parser_object     = None
        self._parser_function   = None
        if parser_type in self._class_parsers.keys():
            self._parser_object     = self._class_parsers[parser_type]()
            self._parser_function   = self._parser_object.parse
            self._parser_extension  = self._parser_object.extension
            self._is_save_required  = self._saver.is_save_required(self._parser_extension)
        elif parser_type in self._function_parsers.keys():
            self._parser_function   = self._function_parsers[parser_type]
            self._parser_extension  = self._parser_function.extension
            self._is_save_required  = self._saver.is_save_required(self._parser_extension)
        else:
            logger.error(PARSER_NOT_FOUND_ERROR_MESSAGE)
            self.initialized = False        
            