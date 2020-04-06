from cortex.readers import MindFileReader

from cortex.utils import Connection

from cortex.utils import Messeges

from cortex.protocol import MessagesTyeps, Protocol

from cortex.readers.reader_versions import ReaderVersions

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger					= logging.getLogger(__name__)
logger_loader 			= _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
DEFAULT_HOST			=	'127.0.0.1'
DEFAULT_PORT			=	'8000'
DEFAULT_FILE_PATH		=	'sample.mind.gz'
DEFAULT_FILE_VERSION	=	ReaderVersions.PROTOBUFF

# Setting default protocol	
protocol = Protocol() 
	
def upload_sample(host='', port='', file_path='', version=''):
	"""Sends to the server user's sample file"""
	logger.info("TODO UPDATE Processing data")
	
	# Default parameter resolution
	host 		= host if host else DEFAULT_HOST
	port 		= port if port else DEFAULT_PORT
	file_path 	= file_path if file_path else DEFAULT_FILE_PATH
	version 	= version if version else DEFAULT_FILE_VERSION
	
	# Parse server address
	server_ip_str, server_port_str  = host, port
	server_port_int                 = int(server_port_str)
	
	def SendHelloMessage(connection, user_information):
		hello_message_params = 				\
			user_information.user_id, 		\
			user_information.username, 		\
			user_information.birth_date,	\
			user_information.gender
		hello_message = protocol.get_message(MessagesTyeps.HELLO_MESSAGE)(*hello_message_params)
		connection.send_message(hello_message.serialize())
			
	def ReceiveConfigMessage(connection):
		config_message = protocol.get_message(MessagesTyeps.CONFIG_MESSAGE).read(connection.receive_message())
		return config_message
			
	def SendSnapshotMessage(connection, snapshot, fields):
		snapshot_message = protocol.get_message(MessagesTyeps.SNAPSHOT_MESSAGE)(snapshot, fields)
		connection.send_message(snapshot_message.serialize())
			
	with MindFileReader(file_path, version) as sample_reader:
		with Connection.connect(server_ip_str, server_port_int) as connection:					
			# Sending hello message
			user_information = sample_reader.user_information
			SendHelloMessage(connection, user_information)
			# Receiving confing message
			config_message = ReceiveConfigMessage(connection)
			fields = config_message.fields			
			# Sending snapshot messages
			for snapshot in sample_reader:
				SendSnapshotMessage(connection, snapshot, fields)
	print(Messeges.DONE_MESSEGE)
