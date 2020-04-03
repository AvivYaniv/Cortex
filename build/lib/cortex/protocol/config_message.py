
class ConfigMessage:
    def __init__(self, *args):
        self.fields_number  = len(args)
        self.fields         = args
         
    def __repr__(self):
        return f'ConfigMessage(fields_number={self.fields_number}, fields={self.fields})'
    
    def __str__(self):
        return f'Fields={self.fields}'
    