import io
import time
from struct import pack, calcsize
from datetime import datetime

from cortex.protocol.hello_message import HelloMessage

from cortex.utils import Serialization
from builtins import staticmethod

from cortex.entities import UserInfo

from cortex.utils import TimeUtils

class HelloMessageNative(HelloMessage):
    ENCODING                = 'utf-8' 
    
    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'QI'
    SERIALIZATION_PAYLOAD   = '{0}sIc'
    SERIALIZATION_FORMAT    = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_PAYLOAD
    
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
        username_size                   = len(self.user_info.username)
        birth_date_as_number            = self.user_info.birth_date
        return                                                                  \
            pack(self.get_current_serialization_format(),                       \
                 self.user_info.user_id,                                        \
                 username_size,                                                 \
                 self.user_info.username.encode(HelloMessageNative.ENCODING),   \
                 birth_date_as_number,                                          \
                 self.gender.encode(HelloMessageNative.ENCODING))
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        return HelloMessageNative.read_stream(stream)
    
    @staticmethod
    def read_stream(stream):
        user_id, username_size                                          = \
            Serialization.read(stream, HelloMessageNative.SERIALIZATION_HEADER)
        CURRENT_USER_PAYLOAD_FORMAT = HelloMessageNative.SERIALIZATION_PAYLOAD.format(username_size)
        username, birth_date, gender                                    = \
            Serialization.read(stream, CURRENT_USER_PAYLOAD_FORMAT)
        user_info = UserInfo(user_id, username, birth_date, gender)
        return HelloMessage(user_info)
    