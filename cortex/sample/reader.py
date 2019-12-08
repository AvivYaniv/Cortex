import io

class Reader:
    @staticmethod
    def ReadFromFile(file):
        return Reader.Read(io.open(file))
    
    @staticmethod
    def Read(stream):
        print(stream.readall())
        