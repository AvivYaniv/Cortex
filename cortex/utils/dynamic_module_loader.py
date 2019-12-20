import importlib
import inspect
import os
import pathlib
import sys

class DynamicModuleLoader:
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
            submodule_name = f'cortex.{root.name}.{path.stem}'
            print(f'{caller_file_name} importing {submodule_name}')
            #importlib.import_module(f'{submodule_name}', package=root.name)
            importlib.import_module(f'{submodule_name}', package=__package__)
            imported_modules_names.append(submodule_name)
        return imported_modules_names
    
    @staticmethod
    def dynamic_lookup(imported_modules_names, lookup_token):
        names = set()
        loaded_functions = []
        loaded_classes   = []
        for submodule_name in imported_modules_names:
            submodule = sys.modules[submodule_name]
            loaded_functions.extend(__class__._dynamic_functions_lookup(submodule, lookup_token, names))
            loaded_classes.extend(__class__._dynamic_classess_lookup(submodule, lookup_token, names))
        return (names, loaded_functions, loaded_classes)
    
    @staticmethod
    def _dynamic_functions_lookup(submodule, lookup_token, names):
        loaded_functions = []
        lookup_token = '_' + lookup_token
        functions_list = [(name, obj) for name,obj in inspect.getmembers(submodule) if inspect.isfunction(obj)]
        for name, obj in functions_list:
            if name.endswith(lookup_token):
                loaded_functions.append(obj)
                names.add(obj.field)  
        return loaded_functions  
    
    @staticmethod
    def _dynamic_classess_lookup(submodule, lookup_token, names):
        loaded_classes = []
        lookup_token = lookup_token.capitalize()
        classes_list = [(name, obj) for name,obj in inspect.getmembers(submodule) if inspect.isclass(obj)]
        for name, obj in classes_list:
            if name.endswith(lookup_token):
                loaded_classes.append(obj)
                names.add(obj.field)  
        return loaded_classes
