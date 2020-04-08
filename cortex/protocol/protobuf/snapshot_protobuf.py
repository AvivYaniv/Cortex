import io
import time
import datetime

from cortex.protobuf import protocol_proto

from cortex.entities.snapshot import Snapshot

from cortex.sample.colorimage import ColorImage
from cortex.sample.depthimage import DepthImage

from cortex.protocol.snapshot_message import SnapshotMessage

from cortex.utils import Serialization
from cortex.utils import TimeUtils

class SnapshotMessageProto(SnapshotMessage):
    
    def serialize(self):
        snapshot_message                      	        = protocol_proto.SnapshotMessage()
        snapshot_message.snapshot.datetime    	        = self.snapshot.timestamp
        
        translation                                     = protocol_proto.Pose.Translation()
        translation.x, translation.y, translation.z     = self.snapshot.pose.translation.get()
        rotation                                        = protocol_proto.Pose.Rotation()
        rotation.x, rotation.y, rotation.z, rotation.w  = self.snapshot.pose.rotation.get()
        
        pose                                            = protocol_proto.Pose()
        pose.rotation.CopyFrom(rotation)
        pose.translation.CopyFrom(translation)
        snapshot_message.snapshot.pose.CopyFrom(pose)
        
        color_image                                     = protocol_proto.ColorImage()
        color_image.width, color_image.height, color_image.data =                   \
            self.snapshot.color_image.width, self.snapshot.color_image.height, self.snapshot.color_image.data
        snapshot_message.snapshot.color_image.CopyFrom(color_image)
        
        depth_image                                     = protocol_proto.DepthImage()
        depth_image.width, depth_image.height =                                     \
            self.snapshot.depth_image.width, self.snapshot.depth_image.height
        depth_image.data.extend(self.snapshot.depth_image.data)
        snapshot_message.snapshot.depth_image.CopyFrom(depth_image) 
        
        feelings                                        = protocol_proto.Feelings()
        feelings.hunger, feelings.thirst, feelings.exhaustion, feelings.happiness = \
            self.snapshot.user_feelings.get()
        snapshot_message.snapshot.feelings.CopyFrom(feelings)
         
        return Serialization.serialize_tunnled_message(snapshot_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        return SnapshotMessageProto.read_stream(stream)
    
    @staticmethod
    def read_stream(stream):        
        snapshot_message_bytes         =     Serialization.read_tunnled_message(stream)
        snapshot_message_protobuf      =     protocol_proto.SnapshotMessage()
        snapshot_message_protobuf.ParseFromString(snapshot_message_bytes)
        
        translation                 =                                   \
            (snapshot_message_protobuf.snapshot.pose.translation.x,     \
             snapshot_message_protobuf.snapshot.pose.translation.y,     \
             snapshot_message_protobuf.snapshot.pose.translation.z)
        
        rotation                     =                                  \
            (snapshot_message_protobuf.snapshot.pose.rotation.x,        \
             snapshot_message_protobuf.snapshot.pose.rotation.y,        \
             snapshot_message_protobuf.snapshot.pose.rotation.z,        \
             snapshot_message_protobuf.snapshot.pose.rotation.w)
        
        color_image                    =                                \
            ColorImage(                                                 \
                snapshot_message_protobuf.snapshot.color_image.width,   \
                snapshot_message_protobuf.snapshot.color_image.height,  \
                snapshot_message_protobuf.snapshot.color_image.data)

        depth_image                    =                                \
            DepthImage(                                                 \
                snapshot_message_protobuf.snapshot.depth_image.width,   \
                snapshot_message_protobuf.snapshot.depth_image.height,  \
                snapshot_message_protobuf.snapshot.depth_image.data)
        
        user_feeling                =                                   \
            (snapshot_message_protobuf.snapshot.feelings.hunger,        \
             snapshot_message_protobuf.snapshot.feelings.thirst,        \
             snapshot_message_protobuf.snapshot.feelings.exhaustion,    \
             snapshot_message_protobuf.snapshot.feelings.happiness)
        
        snapshot                     =                                  \
            Snapshot(                                                   \
                     snapshot_message_protobuf.snapshot.datetime,       \
                     translation,                                       \
                     rotation,                                          \
                     color_image,                                       \
                     depth_image,                                       \
                     user_feeling)
        
        return snapshot
        