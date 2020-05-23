import os

from cortex.utils import DynamicModuleLoader

from cortex.protocol import ProtocolMessagesTyeps, Protocol

from cortex.parsers.snapshot.parser_file_handler import ParserFileHandler

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
PARSER_NOT_FOUND_ERROR_MESSAGE  =   'Parser function/class not found in directory'

class ParserHandler:
    LOOKUP_TOKEN        =   'parser'
    NAME_IDENTIFIER     =   'field'
    
    def __init__(self, parser_type):
        self.initialized    = True
        self.protocol       = Protocol() 
        self._file_handler  = ParserFileHandler()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        self._function_parsers, self._class_parsers = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        self._set_parser_function(parser_type)
      
    def read_raw_snapshot(self, raw_snapshot_path):
        raw_snapshot    = self._file_handler.read_file(raw_snapshot_path, 'rb')
        snapshot        = self.protocol.get_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE).read(raw_snapshot)
        return snapshot
    
    def parse_snapshot(self, raw_snapshot):
        try:
            return self._parser_function(raw_snapshot)
        except Exception as e:
            logger.error(f'error parsing raw snapshot : {e}')
            return None
    
    def parse_raw_snapshot_file(self, raw_snapshot_path):
        try:
            snapshot        = self.read_raw_snapshot(raw_snapshot_path)
        except Exception as e:
            logger.error(f'error reading snapshot file {raw_snapshot_path} : {e}')
            return None
        parse_result        = self.parse_snapshot(snapshot)
        if not parse_result:
            return None
        result, metadata    = parse_result
        return (result, snapshot, metadata)
    
    def save_parsed(self, context, result):
        file_path = self._file_handler.get_path(context, self._parser_extension)
        self._file_handler.save_file(file_path, result)
        return file_path
        
    def export_parse(self, context, raw_snapshot_message):
        is_uri                      = False
        parse_result                = self.parse_raw_snapshot_file(raw_snapshot_message.raw_snapshot_path)
        # If error reading snapshot
        if not parse_result:
            return None
        result, snapshot, metadata  = parse_result
        # If error parsing snapshot
        if not result:
            return None    
        if self._is_save_required:
            result                  = self.save_parsed(context, result)
            is_uri                  = True
        return (is_uri, result, snapshot, metadata)

    def _set_parser_function(self, parser_type):
        self._parser_object     = None
        self._parser_function   = None
        if parser_type in self._class_parsers.keys():
            self._parser_object     = self._class_parsers[parser_type]()
            self._parser_function   = self._parser_object.parse
            self._parser_extension  = self._parser_object.extension
            self._is_save_required  = self._file_handler.is_save_required(self._parser_extension)
        elif parser_type in self._function_parsers.keys():
            self._parser_function   = self._function_parsers[parser_type]
            self._parser_extension  = self._parser_function.extension
            self._is_save_required  = self._file_handler.is_save_required(self._parser_extension)
        else:
            logger.error(PARSER_NOT_FOUND_ERROR_MESSAGE)
            self.initialized = False        
            