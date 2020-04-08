
class ConfigMessage:
    def __init__(self, fields_config):
        self.fields_number  = len(fields_config)
        self.fields         = fields_config
         
    def __repr__(self):
        return f'ConfigMessage(fields_number={self.fields_number}, fields={self.fields})'
    
    def __str__(self):
        return f'Fields={self.fields}'
    