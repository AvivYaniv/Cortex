
from cortex.utils import FileReaderDriver

class FileReaderBase:    
    def __init__(self, file_path):
        file_reader_driver  = FileReaderDriver.find_driver(file_path)
        self.stream         = file_reader_driver.open(file_path, 'rb')
    
    def close(self):
        self.stream.close()
    