import os

from cortex.writers.writer_versions import WriterVersions

from cortex.utils import DynamicModuleLoader

DEFAULT_MIND_FILE_VERSION   =   WriterVersions.PROTOBUFF

class MindStreamWriter:
    LOOKUP_TOKEN        =   'writer'
    NAME_IDENTIFIER     =   'version'
        
    def __init__(self, file_path, version=None): 
        version = version if version else DEFAULT_MIND_FILE_VERSION
        self._load_writers()
        writer_class        = self.find_writer_driver(version)
        self.writer         = writer_class(file_path)        

    def _load_writers(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        _, self._sample_writers_drivers = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        
    def find_writer_driver(self, version):
        for writer_version, writer in self._sample_writers_drivers.items():
            if writer_version == version:
                return writer
        return ValueError(f'Invalid writer version: {version}')
        
    def write_user_information(self, user_information):
        return self.writer.write_user_information(user_information)
    
    def write_snapshot(self, snapshot):
        return self.writer.write_snapshot(snapshot)
    
    ### Context Manager ###
    def __enter__(self):
        return self
    
    def __exit__(self, exception, error, traceback):
        self.writer.close()
        
class MindFileWriter(MindStreamWriter):
    def __init__(self, file_path, version=None):
        super().__init__(file_path, version)
