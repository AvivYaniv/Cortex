import importlib
import inspect
import os
import pathlib
import sys

class DynamicModuleLoader:
    @staticmethod
    def get_callers_module_name():
        frm         = inspect.stack()[2]
        mod         = inspect.getmodule(frm[0])
        mod_name    = mod.__name__
        name        = mod_name[:mod_name.rfind('.')]
        return name
    
    @staticmethod
    def load_modules(root): 
        imported_modules_names = []
        root = pathlib.Path(root).absolute()    
        sys.path.insert(0, str(root.parent))
        caller_file_path = inspect.getmodule(inspect.stack()[1][0]).__file__
        caller_file_name = os.path.basename(caller_file_path)
        for path in root.iterdir(): 
            if path.name == caller_file_name    or  \
               path.name.startswith('_')        or  \
               path.name.startswith('__')       or  \
               not path.suffix == '.py':    
                continue    
            caller_module_name  = DynamicModuleLoader.get_callers_module_name()
            submodule_name      = f'{caller_module_name}.{path.stem}'
            importlib.import_module(f'{submodule_name}', package=__package__)
            imported_modules_names.append(submodule_name)
        return imported_modules_names
    
    @staticmethod
    def dynamic_lookup_to_lists(imported_modules_names, lookup_token, name_identifier=None):
        names = set()
        loaded_functions, loaded_classes = \
            __class__.dynamic_lookup_to_dictionary(imported_modules_names, lookup_token, name_identifier)
        names.update(loaded_functions.keys())
        names.update(loaded_classes.keys())
        return (names, loaded_functions.values(), loaded_classes.values())

    @staticmethod
    def dynamic_lookup_to_dictionary(imported_modules_names, lookup_token, name_identifier=None):
        loaded_functions = {}
        loaded_classes   = {}
        for submodule_name in imported_modules_names:
            submodule = sys.modules[submodule_name]
            __class__._dynamic_functions_lookup_to_dictionary(submodule, lookup_token, loaded_functions, name_identifier)
            __class__._dynamic_classess_lookup_to_dictionary(submodule, lookup_token, loaded_classes, name_identifier)
        return (loaded_functions, loaded_classes)
    
    @staticmethod
    def _dynamic_functions_lookup_to_dictionary(submodule, lookup_token, loaded_functions, name_identifier=None):
        lookup_token = '_' + lookup_token
        functions_list = [(name, obj) for name,obj in inspect.getmembers(submodule) if inspect.isfunction(obj)]
        for name, obj in functions_list:
            if name.endswith(lookup_token):
                identifier = name
                if name_identifier and hasattr(obj, name_identifier):
                    identifier = getattr(obj, name_identifier)
                loaded_functions[identifier] = obj 
        
    @staticmethod
    def _dynamic_classess_lookup_to_dictionary(submodule, lookup_token, loaded_classes, name_identifier=None):
        lookup_token = lookup_token.lower()
        classes_list = [(name, obj) for name,obj in inspect.getmembers(submodule) if inspect.isclass(obj)]
        for name, obj in classes_list:
            if name.lower().endswith(lookup_token):
                identifier = name
                if name_identifier and hasattr(obj, name_identifier):
                    identifier = getattr(obj, name_identifier)
                loaded_classes[identifier] = obj 
        