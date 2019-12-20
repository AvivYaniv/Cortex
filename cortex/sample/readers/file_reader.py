import io
import gzip

class FileReaderBase:
    FILE_READER_DRIVERS = { '.mind' : io , '.gz' : gzip }
    
    def __init__(self, file_path):
        file_reader_driver  = self._find_filer_reader_driver(file_path)
        self.stream         = file_reader_driver.open(file_path, 'rb')
    
    def _find_filer_reader_driver(self, file_path):
        for reader_extension, reader_driver in self.FILE_READER_DRIVERS.items():
            if file_path.endswith(reader_extension):
                return reader_driver
        # Default case - binary reader
        return io
    
    def close(self):
        self.stream.close()
    