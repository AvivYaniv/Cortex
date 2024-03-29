import time
from struct import pack, calcsize
from datetime import datetime

from cortex.utils import Serialization
from cortex.utils import TimeUtils

from cortex.entities import UserInfo

class UserInformation:
    ENCODING                = 'utf-8'
    
    ERROR_DATA_INCOMPLETE   = 'incomplete data'

    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'QI'
    SERIALIZATION_PAYLOAD   = '{0}sIc'
    SERIALIZATION_FORMAT    = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_PAYLOAD
    
    GENDER_TABLE            = { 'm' : 'male' , 'f' : 'female', 'o' : 'other' }
    
    def __init__(self, user_id, username, birth_date, gender):
        self.user_id        = user_id
        self.username       = username if isinstance(username, str) else username.decode(UserInformation.ENCODING)
        self.birth_date     = datetime.fromtimestamp(birth_date)
        self.gender         = gender if isinstance(gender, str) else gender.decode(UserInformation.ENCODING)
         
    def __repr__(self):
        return f'UserInformation(user_id={self.user_id}, username={self.username}, birth_date={datetime.strftime(self.birth_date, TimeUtils.DATETIME_FORMAT)}, gender={self.gender})'
    
    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {datetime.strftime(self.birth_date, TimeUtils.CONCISE_DATE_FORMAT)} ({UserInformation.GENDER_TABLE[self.gender]})'
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):        
            username_size = len(self.username)
            
            # user_id        :    uint64
            # username       :    uint32 + string of <username_size> length
            # birth_date     :    uint32
            # gender         :    char
            self._current_serialization_format = UserInformation.SERIALIZATION_FORMAT.format(username_size)
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        username_size                   = len(self.username)
        birth_date_as_number            = int(time.mktime(self.birth_date.timetuple()))
        return                                                      \
            pack(self.get_current_serialization_format(),           \
                 self.user_id,                                      \
                 username_size,                                     \
                 self.username.encode(UserInformation.ENCODING),    \
                 birth_date_as_number,                              \
                 self.gender.encode(UserInformation.ENCODING))
    
    @staticmethod
    def read(stream):
        user_id, username_size                          = \
            Serialization.read(stream, UserInformation.SERIALIZATION_HEADER)        
        CURRENT_USER_PAYLOAD_FORMAT                     = UserInformation.SERIALIZATION_PAYLOAD.format(username_size)
        username, birth_date, gender                    = \
            Serialization.read(stream, CURRENT_USER_PAYLOAD_FORMAT)
        return UserInfo(user_id, username, datetime.fromtimestamp(birth_date), gender)
    