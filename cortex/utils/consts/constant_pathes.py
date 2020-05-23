
import pathlib
from inspect import getsourcefile
from os.path import abspath

from cortex.utils.files.file_handler import _FileHandler

def project_root():
    return str(pathlib.Path(abspath(getsourcefile(lambda:0))).parent.parent.parent.parent)

def expand_file_path_relative_to_project_root(file_path):
    return str(pathlib.Path(project_root(), file_path))

class ConstantPathes:
    DATA_DIRRECTORY         =   'data'
    SNAPSHOTS_DIRRECTORY    =   'snapshots'
    
    @staticmethod
    def get_snapshots_path():
        return _FileHandler.to_safe_file_path(      \
                ConstantPathes.DATA_DIRRECTORY,     \
                ConstantPathes.SNAPSHOTS_DIRRECTORY)
    