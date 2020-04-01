import io
import time

from cortex.protobuf import protocol_proto

from cortex.protocol.snapshot_message import SnapshotMessage

from cortex.utils.serialization import Serialization

class SnapshotMessageProto(SnapshotMessage):
    
    def serialize(self):
        snapshot_message                      = protocol_proto.Snapshot()
        snapshot_message.datetime    		  = int(time.mktime(self.datetime.timetuple()))
        snapshot_message.user_data.username   = self.username  
        snapshot_message.user_data.birthday   = 
        snapshot_message.user_data.gender     = HelloMessageProto.GENDER_TABLE[self.gender].number
        return Serialization.serialize_tunnled_message(snapshot_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        
        user_information_bytes         =     Serialization.read_tunnled_message(stream)
        user_information_protobuf      =     protocol_proto.Hello()
        user_information_protobuf.ParseFromString(user_information_bytes)
        
        user_information                 =                          \
            HelloMessage(                                           \
                    user_information_protobuf.user_data.user_id,    
                    user_information_protobuf.user_data.username, 
                    user_information_protobuf.user_data.birthday, 
                    protocol_proto._USER_GENDER.values_by_number[user_information_protobuf.user_data.gender].name.lower()[0])       
        return user_information
        