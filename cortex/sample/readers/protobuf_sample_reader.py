import gzip

from cortex.protobuf import cortex_pb2 as protobuf

from cortex.sample.snapshot import Snapshot
from cortex.sample.userinformation import UserInformation

from cortex.utils import Serialization
from cortex.sample.colorimage import ColorImage
from cortex.sample.depthimage import DepthImage

class ProtobufSampleReader:
	
	version 			= 'v2'
	
	PROTOBUF_HEADER		=	'I'
	
	GENDER_TABLE		= { 0 : 'm', 1 : 'f', 2 : 'o' }
	
	def __init__(self, file_path):
		self.stream = gzip.open(file_path, 'rb')
		
	def close(self):
		self.stream.close()
		
	def read_protobuf_message(self):
		message_size = Serialization.read(self.stream, ProtobufSampleReader.PROTOBUF_HEADER, expect_eof=True)[0]
		return self.stream.read(message_size)
		
	def read_user_information(self):
		user_information_bytes 		= 	self.read_protobuf_message()
		user_information_protobuf 	= 	protobuf.User()
		user_information_protobuf.ParseFromString(user_information_bytes)
		
		user_information 			=							\
			UserInformation(									\
							user_information_protobuf.user_id, 	\
							user_information_protobuf.username, 
							user_information_protobuf.birthday, 
							ProtobufSampleReader.GENDER_TABLE[user_information_protobuf.gender])
		
		return user_information
	
	def read_snapshot(self):
		snapshot_bytes 				= 	self.read_protobuf_message()
		snapshot_protobuf 			= 	protobuf.Snapshot()
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
				snapshot_protobuf.depth_image.height, 			\
				snapshot_protobuf.depth_image.width,			\
				snapshot_protobuf.depth_image.data)
		
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
