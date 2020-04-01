import io
import time

from cortex.protobuf import protocol_proto

from cortex.protocol.snapshot_message import SnapshotMessage

from cortex.utils.serialization import Serialization

class SnapshotMessageProto(SnapshotMessage):
    
    def serialize(self):
        snapshot_message                      	= protocol_proto.SnapshotMessage()
        snapshot_message.snapshot.datetime    	= int(time.mktime(self.datetime.timetuple()))
        snapshot_message.snapshot.pose   		= self.pose        
        snapshot_message.snapshot.color_image   = self.color_image
        snapshot_message.snapshot.depth_image   = self.depth_image 
        snapshot_message.snapshot.feelings   	= self.feelings 
        return Serialization.serialize_tunnled_message(snapshot_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        
        snapshot_message_bytes         =     Serialization.read_tunnled_message(stream)
        snapshot_message_protobuf      =     protocol_proto.SnapshotMessage()
        snapshot_message_protobuf.ParseFromString(snapshot_message_bytes)
        
        user_information                 =                          \
            HelloMessage(                                           \
                    user_information_protobuf.user_data.user_id,    
                    user_information_protobuf.user_data.username, 
                    user_information_protobuf.user_data.birthday, 
                    protocol_proto._USER_GENDER.values_by_number[user_information_protobuf.user_data.gender].name.lower()[0])       
        return user_information
        