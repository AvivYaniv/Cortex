import os

from cortex.readers.reader_versions import ReaderVersions

from cortex.utils import DynamicModuleLoader

class SampleStreamReader:
    LOOKUP_TOKEN        =   'reader'
    NAME_IDENTIFIER     =   'version'
        
    def __init__(self, file_path, version): 
        self._load_readers()
        reader_class        = self.find_reader_driver(version)
        self.reader         = reader_class(file_path)
        self._read_user_information()

    def _load_readers(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
        _, self._sample_readers_drivers = \
            DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, self.LOOKUP_TOKEN, self.NAME_IDENTIFIER)
        
    def find_reader_driver(self, version):
        for reader_version, reader in self._sample_readers_drivers.items():
            if reader_version == version:
                return reader
        return ValueError(f'Invalid reader version: {version}')
        
    def _read_user_information(self):
        user_information    = self.reader.read_user_information()
        # Copy user_information fields
        for field in user_information.__dict__:
            if field not in self.__dict__:
                self.__dict__[field] = user_information.__dict__[field]
        self.user_information = user_information
        
    ### Context Manager ###
    def __enter__(self):
        return self
    
    def __exit__(self, exception, error, traceback):
        self.reader.close()
        
    ### Iterator ###        
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.reader.read_snapshot()

class SampleFileReader(SampleStreamReader):
    def __init__(self, file_path, version=ReaderVersions.PROTOBUFF):
        super().__init__(file_path, version)

def read(file_path):
    with SampleFileReader(file_path, version=ReaderVersions.PROTOBUFF) as sample_reader:
        print(str(sample_reader.user_information))
        for snapshot in sample_reader:
            print(str(snapshot))
