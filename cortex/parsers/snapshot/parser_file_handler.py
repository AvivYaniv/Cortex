
from cortex.utils import _FileHandler

from cortex.utils import ConstantPathes

class ParserFileHandler:
    EXTENSIONS_TO_SAVE  =   [ '.png', '.gif', '.jpg', '.jpeg', '.wma', '.wmv', '.mp4', '.avi', '.mov', '.flv' ]
    
    def __init__(self):
        self.file_handler   = _FileHandler()
        
    def get_path(self, context, extension=''):
        file_path   =                                   \
            _FileHandler.to_safe_file_path(             \
                ConstantPathes.get_snapshots_path(),    \
                context.user_id,                        \
                context.snapshot_uuid,                  \
                fname=context.parser_type,              \
                extension=extension)
        return file_path
    
    @staticmethod
    def is_save_required(extension):
        return extension.lower() in ParserFileHandler.EXTENSIONS_TO_SAVE
    
    @staticmethod
    def create_path(path):
        _FileHandler.create_path(path)
        
    def read_file(self, file_path, mode=None):
        return self.file_handler.read_file(file_path, mode)
        
    def save_file(self, file_path, data, mode=None):
        mode = mode if mode else 'wb'
        self.file_handler.save(file_path, data, mode)
        
    def save(self, context, data, extension=''):
        file_path   = self.get_path(context, extension)
        self.file_handler.save(file_path, data)
