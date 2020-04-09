
from cortex.utils import _FileHandler

from cortex.utils import ConstantPathes

class ParserSaver:
    EXTENSIONS_TO_SAVE  =   [ '.png', '.gif', '.jpg', '.jpeg', '.wmawmv', '.mp4', '.avi', '.mov', '.flv' ]
    
    def __init__(self):
        self.file_handler   = _FileHandler()
        
    def get_path(self, context, extension=''):
        file_path   =                                   \
            _FileHandler.to_safe_file_path(             \
                ConstantPathes.DATA_DIRRECTORY,         \
                ConstantPathes.SNAPSHOTS_DIRRECTORY,    \
                context.user_id,                        \
                context.snapshot_uuid,                  \
                fname=context.parser_type,              \
                extension=extension)
        return file_path
    
    @staticmethod
    def is_save_required(extension):
        return extension.lower() in ParserSaver.EXTENSIONS_TO_SAVE
    
    @staticmethod
    def create_path(path):
        _FileHandler.create_path(path)
        
    def save_file(self, file_path, data, mode=None):
        mode = mode if mode else 'wb'
        self.file_handler.save(file_path, data, mode)
        
    def save(self, context, data, extension=''):
        file_path   = self.get_path(context, extension)
        self.file_handler.save(file_path, data)
