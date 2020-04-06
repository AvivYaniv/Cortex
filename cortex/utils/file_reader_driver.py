import io
import gzip

class FileReaderDriver:
    @staticmethod
    def find_driver(file_path):
        FILE_READER_DRIVERS = { '.gz' : gzip }
        for reader_extension, reader_driver in FILE_READER_DRIVERS.items():
            if file_path.endswith(reader_extension):
                return reader_driver
        # Default case - binary reader
        return io
    