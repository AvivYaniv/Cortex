from cortex.protobuf import mind_proto

from cortex.entities import Snapshot
from cortex.entities import UserInfo

from cortex.utils import Serialization
from cortex.sample.colorimage import ColorImage
from cortex.sample.depthimage import DepthImage

from cortex.readers.file_reader import FileReaderBase

class ProtobufMindReader(FileReaderBase):
	
	version 			= 'protobuf'
	
	PROTOBUF_HEADER		= 'I'
	
	GENDER_TABLE		= { 0 : 'm', 1 : 'f', 2 : 'o' }
	
	def __init__(self, file_path):
		super().__init__(file_path)
		
	def read_user_information(self):
		user_information_bytes 		= 	Serialization.read_tunnled_message(self.stream)
		user_information_protobuf 	= 	mind_proto.User()
		user_information_protobuf.ParseFromString(user_information_bytes)
		
		user_information 			=							\
			UserInfo(											\
							user_information_protobuf.user_id, 	\
							user_information_protobuf.username, 
							user_information_protobuf.birthday, 
							mind_proto._USER_GENDER.values_by_number[user_information_protobuf.gender].name.lower()[0])
		
		return user_information
	
	def read_snapshot(self):
		snapshot_bytes 				= 	Serialization.read_tunnled_message(self.stream, expect_eof=True)
		snapshot_protobuf 			= 	mind_proto.Snapshot()
		snapshot_protobuf.ParseFromString(snapshot_bytes)
		
		translation 				= 							\
			(snapshot_protobuf.pose.translation.x, 				\
			 snapshot_protobuf.pose.translation.y, 				\
			 snapshot_protobuf.pose.translation.z)
		
		rotation 					= 							\
			(snapshot_protobuf.pose.rotation.x, 				\
			 snapshot_protobuf.pose.rotation.y, 				\
			 snapshot_protobuf.pose.rotation.z, 				\
			 snapshot_protobuf.pose.rotation.w)
		
		color_image					=							\
			ColorImage(											\
				snapshot_protobuf.color_image.width, 			\
				snapshot_protobuf.color_image.height,			\
				snapshot_protobuf.color_image.data)

		depth_image					=							\
			DepthImage(											\
				snapshot_protobuf.depth_image.width, 			\
				snapshot_protobuf.depth_image.height,			\
				snapshot_protobuf.depth_image.data)
		
		depth_image._fix_hardware_size()
		
		user_feeling				=							\
			(snapshot_protobuf.feelings.hunger, 				\
			 snapshot_protobuf.feelings.thirst, 				\
			 snapshot_protobuf.feelings.exhaustion,				\
			 snapshot_protobuf.feelings.happiness)
		
		snapshot 					= 							\
			Snapshot(											\
					 snapshot_protobuf.datetime,				\
					 translation, 								\
					 rotation, 									\
					 color_image, 								\
					 depth_image, 								\
					 user_feeling)
		
		return snapshot
