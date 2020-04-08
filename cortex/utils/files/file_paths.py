import os
import inspect

EXTENSTION_DAFULT   =   ''

def get_project_file_path_by_caller(fname, extension=None):
    extension = extension if extension else EXTENSTION_DAFULT
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    return os.path.join(os.path.dirname(os.path.realpath(filename)), fname + extension)
