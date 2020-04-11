
from cortex.utils import dictionary_to_json

class JSONMarshal:
    type    =   'json'
    
    def marshal(self, dictionary):
        return dictionary_to_json(dictionary)
