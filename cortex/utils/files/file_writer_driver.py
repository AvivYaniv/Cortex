import io
import gzip

class FileWriterDriver:
    @staticmethod
    def find_driver(file_path):
        FILE_WRITER_DRIVERS = { '.gz' : gzip }
        for writer_extension, writer_driver in FILE_WRITER_DRIVERS.items():
            if file_path.endswith(writer_extension):
                return writer_driver
        # Default case - binary writer
        return io
    