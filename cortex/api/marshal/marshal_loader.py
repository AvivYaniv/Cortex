import os

from cortex.utils import DynamicModuleLoader

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
MARSHAL_NOT_FOUND_ERROR_MESSAGE  =   'marshal function/class not found in directory'

class marshalLoader:
    LOOKUP_TOKEN        =   'marshal'
    NAME_IDENTIFIER     =   'type'
    
    def __init__(self, marshal_type):
        self.initialized    = True
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        self._function_marshals, self._class_marshals = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        self._set_marshal_function(marshal_type)
      
    def marshal(self, dictionary):
        if not self.initialized:
            return ''
        return self._marshal_function(dictionary)
    
    def _set_marshal_function(self, marshal_type):
        self._marshal_object          = None
        self._marshal_function        = None
        if marshal_type in self._class_marshals.keys():
            self._marshal_object      = self._class_marshals[marshal_type]()
            self._marshal_function    = self._marshal_object.marshal                     
        elif marshal_type in self._function_marshals.keys():
            self._marshal_function    = self._function_marshals[marshal_type]            
        else:
            logger.error(MARSHAL_NOT_FOUND_ERROR_MESSAGE)
            self.initialized = False
            
            