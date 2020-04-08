
from cortex.utils import json_to_object, object_to_json

class JsonMessage:
    def serialize(self):
        return object_to_json(self)
        
    @staticmethod
    def deserialize(data, cls = None):
        converted = json_to_object(data)
        if cls:
            converted.__class__ = cls
        return converted
