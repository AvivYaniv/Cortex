import io
import time

from cortex.protobuf import protocol_proto

from cortex.protocol.hello_message import HelloMessage

from cortex.utils import Serialization

from cortex.entities import UserInfo

class HelloMessageProto(HelloMessage):
    
    GENDER_TABLE            =                                               \
        {                                                                   \
            'm' : protocol_proto._USER_GENDER.values_by_name["MALE"] ,      \
            'f' : protocol_proto._USER_GENDER.values_by_name["FEMALE"] ,    \
            'o' : protocol_proto._USER_GENDER.values_by_name["OTHER"]       \
        }

    def serialize(self):
        hello_message                      = protocol_proto.HelloMessage()
        hello_message.user_data.user_id    = self.user_info.user_id   
        hello_message.user_data.username   = self.user_info.username  
        hello_message.user_data.birthday   = self.user_info.birth_date
        hello_message.user_data.gender     = HelloMessageProto.GENDER_TABLE[self.user_info.gender].number
        return Serialization.serialize_tunnled_message(hello_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        return HelloMessageProto.read_stream(stream)
    
    @staticmethod
    def read_stream(stream):
        hello_message_bytes         =     Serialization.read_tunnled_message(stream)
        hello_message_protobuf      =     protocol_proto.HelloMessage()
        hello_message_protobuf.ParseFromString(hello_message_bytes)
        user_info                   =                                                                               \
            UserInfo(                                                                                               \
            hello_message_protobuf.user_data.user_id,                                                               \
            hello_message_protobuf.user_data.username,                                                              \
            hello_message_protobuf.user_data.birthday,                                                              \
            protocol_proto._USER_GENDER.values_by_number[hello_message_protobuf.user_data.gender].name.lower()[0]   \
            )
        return HelloMessage(user_info)
    