
from struct import pack, calcsize

from cortex.writers.file_writer import FileWriterBase

from cortex.sample import Sample

from cortex.utils import Serialization

class BinaryMindWriter(FileWriterBase):
	ENCODING						= 'utf-8' 
	
	SERIALIZATION_ENDIANITY 		= '<'

	SERIALIZATION_HEADER_USER_INFO	= 'QI'
	SERIALIZATION_PAYLOAD_USER_INFO	= '{0}sIc'
	SERIALIZATION_FORMAT_USER_INFO	= SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER_USER_INFO + SERIALIZATION_PAYLOAD_USER_INFO
	
	SERIALIZATION_HEADER_SNAPSHOT 	= 'Qddddddd'
	SERIALIZATION_TRAILER_SNAPSHOT 	= 'ffff'

	version = 'binary'
	
	def __init__(self, file_path):
		super().__init__(file_path)		
			
	def get_user_info_serialization_format(self, user_info):
		username_size = len(user_info.username)  		
		return BinaryMindWriter.SERIALIZATION_FORMAT_USER_INFO.format(username_size)
			
	def write_user_information(self, user_info):
		username_size                   = len(user_info.username)
		birth_date_as_number            = user_info.birth_date
		user_info_bytes_untunneled		= 																		\
			pack(self.get_user_info_serialization_format(user_info), 											\
		         user_info.user_id,                                        										\
		         username_size,                                                 								\
		         user_info.username.encode(BinaryMindWriter.ENCODING),   										\
		         birth_date_as_number,                                          								\
		         self.gender.encode(BinaryMindWriter.ENCODING))
		user_info_bytes			= Serialization.serialize_tunnled_message(user_info_bytes_untunneled)
		self.stream.write(user_info_bytes)
		return len(user_info_bytes)
	
	def write_snapshot(self, snapshot):
		header =                                                                                                \
			pack(BinaryMindWriter.SERIALIZATION_ENDIANITY + BinaryMindWriter.SERIALIZATION_HEADER_SNAPSHOT,		\
				snapshot.timestamp,                                                                        		\
				*snapshot.pose.translation.get(),                                                          		\
				*snapshot.pose.rotation.get())
		body 						=                                                                         	\
			snapshot.color_image.serialize() + snapshot.depth_image.serialize()    
		trailer 					=                                                                           \
		  	pack(BinaryMindWriter.SERIALIZATION_ENDIANITY + BinaryMindWriter.SERIALIZATION_TRAILER_SNAPSHOT,	\
		       	*snapshot.user_feeling.get())
		snapshot_bytes_untunneled	= header + body + trailer
		snapshot_bytes				= Serialization.serialize_tunnled_message(snapshot_bytes_untunneled)
		self.stream.write(snapshot_bytes)
		return len(snapshot_bytes)
