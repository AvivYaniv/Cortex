from cortex.protobuf import mind_proto

from cortex.entities import Snapshot
from cortex.entities import UserInfo

from cortex.utils import Serialization
from cortex.sample.colorimage import ColorImage
from cortex.sample.depthimage import DepthImage

from cortex.writers.file_writer import FileWriterBase

class ProtobufMindWriter(FileWriterBase):
	
	version 			= 'protobuf'
	
	PROTOBUF_HEADER		= 'I'
	
	GENDER_TABLE		= { 'm' : 0 , 'f' : 1 , 'o' : 2 }
	
	def __init__(self, file_path):
		super().__init__(file_path)
		
	def write_user_information(self, user_info):
		proto_user            							= mind_proto.User()
		proto_user.user_id    							= user_info.user_id   
		proto_user.username   							= user_info.username  
		proto_user.birthday   							= user_info.birth_date
		proto_user.gender     							= ProtobufMindWriter.GENDER_TABLE[user_info.gender]
		proto_user_bytes								= Serialization.serialize_tunnled_message(proto_user.SerializeToString())
		self.stream.write(proto_user_bytes)
		return len(proto_user_bytes)
		
	def write_snapshot(self, snapshot):	
		proto_snapshot      							= mind_proto.Snapshot()		
		proto_snapshot.datetime    	        			= snapshot.timestamp
		
		translation                                     = mind_proto.Pose.Translation()
		translation.x, translation.y, translation.z     = snapshot.pose.translation.get()
		rotation                                        = mind_proto.Pose.Rotation()
		rotation.x, rotation.y, rotation.z, rotation.w  = snapshot.pose.rotation.get()
		
		pose                                            = mind_proto.Pose()
		pose.rotation.CopyFrom(rotation)
		pose.translation.CopyFrom(translation)
		proto_snapshot.pose.CopyFrom(pose)
		
		color_image                                     = mind_proto.ColorImage()
		color_image.width, color_image.height, color_image.data =                   \
		    snapshot.color_image.width, snapshot.color_image.height, snapshot.color_image.data
		proto_snapshot.color_image.CopyFrom(color_image)
		
		depth_image                                     = mind_proto.DepthImage()
		depth_image.width, depth_image.height =                                     \
		    snapshot.depth_image.width, snapshot.depth_image.height
		depth_image.data.extend(snapshot.depth_image.data)
		proto_snapshot.depth_image.CopyFrom(depth_image) 
		
		feelings                                        = mind_proto.Feelings()
		feelings.hunger, feelings.thirst, feelings.exhaustion, feelings.happiness = \
		    snapshot.user_feelings.get()
		proto_snapshot.feelings.CopyFrom(feelings)
		
		proto_snapshot_bytes							= Serialization.serialize_tunnled_message(proto_snapshot.SerializeToString())
		self.stream.write(proto_snapshot_bytes)
		return len(proto_snapshot_bytes)
	