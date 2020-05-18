
import ast

class StructuredFile:
    def __init__(self, file_path):
        self.file_path = file_path
    def read_lines(self):
        line_lists = []
        with open(self.file_path, 'r') as f:
            for content in f.readlines():
                parsed  = ast.literal_eval(content)
                line_lists.append(parsed)
        return line_lists
    def append_line(self, content):
        with open(self.file_path, 'a') as f:
            f.write(f'{str(content)}\n')
            