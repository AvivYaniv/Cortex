from cortex.protocol import HelloMessageNative, ConfigMessageNative, SnapshotMessageNative

from cortex.readers import SampleFileReader

from cortex.utils import Connection

from cortex.utils import Messeges

import logging
from cortex.logger import LoggerLoader

# Log loading
logger					= logging.getLogger(__name__)
logger_loader 			= LoggerLoader()
logger_loader.load_log_config()

# Message Classes	
from cortex.protocol import HelloMessageProto, ConfigMessageProto, SnapshotMessageProto
hello_message_class, config_message_class, snapshot_message_class = \
	HelloMessageProto, ConfigMessageProto, SnapshotMessageProto
	
def upload_sample(address, file_path, version):
	"""Sends to the server user's sample file"""
	logger.info("TODO UPDATE Processing data")
	
	# Parse server address
	server_ip_str, server_port_str  = address.split(":")
	server_port_int                 = int(server_port_str)
	
	def SendHelloMessage(connection, user_information):
		hello_message_params = 				\
			user_information.user_id, 		\
			user_information.username, 		\
			user_information.birth_date,	\
			user_information.gender
		hello_message = hello_message_class(*hello_message_params)
		connection.send_message(hello_message.serialize())
			
	def ReceiveConfigMessage(connection):
		config_message = config_message_class.read(connection.receive_message())
		return config_message
			
	def SendSnapshotMessage(connection, snapshot, fields):
		snapshot_message = snapshot_message_class(snapshot, fields)
		connection.send_message(snapshot_message.serialize())
			
	with SampleFileReader(file_path, version) as sample_reader:
		with Connection.connect(server_ip_str, server_port_int) as connection:					
			# Sending hello message
			user_information = sample_reader.user_information
			SendHelloMessage(connection, user_information)
			# Receiving config message
			config_message = ReceiveConfigMessage(connection)
			fields = config_message.fields			
			# Sending snapshot messages
			for snapshot in sample_reader:
				SendSnapshotMessage(connection, snapshot, fields)
	print(Messeges.DONE_MESSEGE)
