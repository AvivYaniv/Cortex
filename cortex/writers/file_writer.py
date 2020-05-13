
from cortex.utils import FileWriterDriver

class FileWriterBase:
    def __init__(self, file_path):
        file_writer_driver          = FileWriterDriver.find_driver(file_path)
        self.stream                 = file_writer_driver.open(file_path, 'wb')
    
    def close(self):
        self.stream.close()
    