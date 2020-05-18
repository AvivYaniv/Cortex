
import ast

class DictionaryFile:
    def __init__(self, file_path):
        self.file_path = file_path
    def read_dictionary(self):
        file_dictionary = {}
        for dictionary in self.read_lines():
            for k, v in dictionary.items():
                if k not in file_dictionary:
                    file_dictionary[k] = []
                file_dictionary[k].append(v)
        return file_dictionary
    def read_lines(self):
        dictionaries = []
        with open(self.file_path, 'r') as f:
            for content in f.readlines():
                parsed  = ast.literal_eval(content)
                dictionaries.append(parsed)
        return dictionaries
    def append_line(self, key, value):
        with open(self.file_path, 'a') as f:
            f.write(f'{{ \"{key}\" : \"{value}\" }}\n')
