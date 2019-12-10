import io

from .sample import Sample

class SampleStreamReader:
    def __init__(self, stream): 
        self.stream = stream
        self._read_user_information()
        
    def _read_user_information(self):
        self.generator      = Sample.read(stream=self.stream)
        user_information    = next(self.generator)
        # Copy user_information fields
        for field in user_information.__dict__:
            if field not in self.__dict__:
                self.__dict__[field] = user_information.__dict__[field]
        self.user_information = user_information
        
    ### Context Manager ###
    def __enter__(self):
        return self
    
    def __exit__(self, exception, error, traceback):
        self.stream.close()
        
    ### Iterator ###        
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.generator)
            
class SampleFileReader(SampleStreamReader):
    def __init__(self, file, mode='rb'):
        super().__init__(io.open(file, mode))

def read(file):
    with SampleFileReader(file) as sample_reader:
        print(str(sample_reader.user_information))
        for snapshot in sample_reader:
            print(str(snapshot))
