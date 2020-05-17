
import os

import functools 

def change_direcoty_to_project_root():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):            
            # Fetch original working directory
            original_working_directory = os.getcwd()            
            # Change working directory up, three time, as this is where relatively to this file is project root
            os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/' + '../' * 3)
            result = function(*args, **kwargs)
            # Restore to original working directory
            os.chdir(original_working_directory)
            return result
        return wrapper
    return decorator
