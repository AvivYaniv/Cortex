
from .yaml_dictionary_reader import yaml_file_to_dictionary_reader

class DictionayReaderDriver:
    @staticmethod
    def find_driver(fname):
        DICTIONARY_FILE_READERS = { '.yaml' : yaml_file_to_dictionary_reader }
        for driver_extenstion in DICTIONARY_FILE_READERS:
            if fname.endswith(driver_extenstion):
                return DICTIONARY_FILE_READERS[driver_extenstion]
        return None
    