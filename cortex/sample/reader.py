import io

from .sample import Sample

class Reader:
    @staticmethod
    def ReadFromFile(file, mode='rb'):
        return Reader.Read(io.open(file, mode))
    
    @staticmethod
    def Read(stream):
        generator = Sample.deserialize(stream=stream)
        
        user_information = generator.__next__()
        
        print(str(user_information))
        
        for snapshot in generator:
            print(snapshot)
        
        
def read(file):
    Reader.ReadFromFile(file)
    