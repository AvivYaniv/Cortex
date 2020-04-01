import io
import time
from struct import pack, calcsize
from datetime import datetime

from ..hello import HelloMessage

from cortex.utils.serialization import Serialization

class HelloMessageNative(HelloMessage):
    ENCODING                = 'utf-8' 
    
    DATETIME_FORMAT         = '%Y-%m-%d_%H:%M:%S'
    CONCISE_DATE_FORMAT     = '%d %B, %Y'

    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'QI'
    SERIALIZATION_PAYLOAD   = '{0}sIc'
    SERIALIZATION_FORMAT    = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_PAYLOAD
    
    GENDER_TABLE            = { 'm' : 'MALE' , 'f' : 'FEMALE', 'o' : 'OTHER' }
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):        
            username_size = len(self.username)
            
            # user_id        :    uint64
            # username       :    uint32 + string of <username_size> length
            # birth_date     :    uint32
            # gender         :    char
            self._current_serialization_format = HelloMessageNative.SERIALIZATION_FORMAT.format(username_size)
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        username_size                   = len(self.username)
        birth_date_as_number            = int(time.mktime(self.birth_date.timetuple()))
       
        return                                                          \
            pack(self.get_current_serialization_format(),               \
                 self.user_id,                                          \
                 username_size,                                         \
                 self.username.encode(HelloMessageNative.ENCODING),     \
                 birth_date_as_number,                                  \
                 self.gender.encode(HelloMessageNative.ENCODING))
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        
        user_id, username_size                          = \
            Serialization.read(stream, HelloMessageNative.SERIALIZATION_HEADER)
        
        CURRENT_USER_PAYLOAD_FORMAT                     = HelloMessageNative.SERIALIZATION_PAYLOAD.format(username_size)
        
        username, birth_date, gender                    = \
            Serialization.read(stream, CURRENT_USER_PAYLOAD_FORMAT)
        
        return HelloMessage(user_id, username, birth_date, gender)
    
    