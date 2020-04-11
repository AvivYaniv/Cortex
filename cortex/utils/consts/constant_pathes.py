
from cortex.utils.files.file_handler import _FileHandler

class ConstantPathes:
    DATA_DIRRECTORY         =   'data'
    SNAPSHOTS_DIRRECTORY    =   'snapshots'
    
    @staticmethod
    def get_snapshots_path():
        return _FileHandler.to_safe_file_path(      \
                ConstantPathes.DATA_DIRRECTORY,     \
                ConstantPathes.SNAPSHOTS_DIRRECTORY)
    