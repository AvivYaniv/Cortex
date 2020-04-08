
from datetime import datetime

DEFAULT_ENCODING            = 'utf-8'

class UserInfo:
    def __init__(self, user_id, username, birth_date, gender, encoding=None):
        encoding            = encoding if encoding else DEFAULT_ENCODING
        self.user_id        = user_id
        self.username       = username if isinstance(username, str) else username.decode(encoding)
        self.birth_date     = datetime.fromtimestamp(birth_date)
        self.gender         = gender if isinstance(gender, str) else gender.decode(encoding)
        