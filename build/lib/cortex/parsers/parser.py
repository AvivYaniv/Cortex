import os

from cortex.utils import DynamicModuleLoader

class Parser:
    LOOKUP_TOKEN        =   'parser'
    NAME_IDENTIFIER     =   'field'
    
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        self.field_names, self._function_parsers, self._class_parsers = \
            DynamicModuleLoader.dynamic_lookup_to_lists(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        self._create_parser_objects()

    def get_fields_names(self):
        return self.field_names
    
    def parse(self, context, snapshot):        
        for f in self._function_parsers:            
            f(context, snapshot)
        for o in self._parser_objects:
            o.parse(context, snapshot)

    def _create_parser_objects(self):
        self._parser_objects = [c() for c in self._class_parsers]
