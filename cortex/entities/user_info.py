
from datetime import datetime

from cortex.utils import object_to_json, json_to_object

DEFAULT_ENCODING            = 'utf-8'

class UserInfo:
    def __init__(self, user_id, username, birth_date, gender, encoding=None):
        encoding            = encoding if encoding else DEFAULT_ENCODING
        self.user_id        = user_id
        self.username       = username if isinstance(username, str) else username.decode(encoding)
        self.birth_date     = birth_date
        self.gender         = gender if isinstance(gender, str) else gender.decode(encoding)
    def serialize(self):
        return object_to_json(self)
    
    @staticmethod
    def deserialize(json_str):
        return json_to_object(json_str)
    