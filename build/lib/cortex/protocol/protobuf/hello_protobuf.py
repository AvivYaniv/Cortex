import io
import time

from cortex.protobuf import protocol_proto

from cortex.protocol.hello_message import HelloMessage

from cortex.utils import Serialization

class HelloMessageProto(HelloMessage):
    
    GENDER_TABLE            =                                               \
        {                                                                   \
            'm' : protocol_proto._USER_GENDER.values_by_name["MALE"] ,      \
            'f' : protocol_proto._USER_GENDER.values_by_name["FEMALE"] ,    \
            'o' : protocol_proto._USER_GENDER.values_by_name["OTHER"]       \
        }

    def serialize(self):
        hello_message                      = protocol_proto.HelloMessage()
        hello_message.user_data.user_id    = self.user_id   
        hello_message.user_data.username   = self.username  
        hello_message.user_data.birthday   = int(time.mktime(self.birth_date.timetuple()))
        hello_message.user_data.gender     = HelloMessageProto.GENDER_TABLE[self.gender].number
        return Serialization.serialize_tunnled_message(hello_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        
        hello_message_bytes         =     Serialization.read_tunnled_message(stream)
        hello_message_protobuf      =     protocol_proto.HelloMessage()
        hello_message_protobuf.ParseFromString(hello_message_bytes)
        
        hello_message                 =                             \
            HelloMessage(                                           \
                    hello_message_protobuf.user_data.user_id,    
                    hello_message_protobuf.user_data.username, 
                    hello_message_protobuf.user_data.birthday, 
                    protocol_proto._USER_GENDER.values_by_number[hello_message_protobuf.user_data.gender].name.lower()[0])       
        return hello_message
        