import os.path

from cortex.readers import MindFileReader

from cortex.utils import Connection

from cortex.utils import Messeges

from cortex.protocol import ProtocolMessagesTyeps, Protocol

from cortex.readers.reader_versions import ReaderVersions

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger					= logging.getLogger(__name__)
logger_loader 			= _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
UPLOAD_SAMPLE_FILE_HAS_FINISHED_INFO_MESSAGE	=	'Upload sample file has finished'
SAMPLE_FILE_NOT_FOUND_ERROR_MESSAGE				=	'Sample file not found'

# Setting default protocol	
protocol = Protocol() 
	
def upload_sample(host='127.0.0.1', port='8000', file_path='sample.mind.gz', version=ReaderVersions.PROTOBUFF):
	"""Sends to the server user's sample file"""
	logger.info('Client uploads sample file {file_path} to server at {host}:{port}')
	# Validating sample file exists - else quitting
	if not os.path.isfile(file_path):
		logger.error(SAMPLE_FILE_NOT_FOUND_ERROR_MESSAGE)
		return	
	# Parse server address
	server_ip_str, server_port_str  = host, port
	server_port_int                 = int(server_port_str)
	# Sends hello message to server
	def SendHelloMessage(connection, user_information):
		hello_message_params = 				\
			user_information.user_id, 		\
			user_information.username, 		\
			user_information.birth_date,	\
			user_information.gender
		hello_message = protocol.get_message(ProtocolMessagesTyeps.HELLO_MESSAGE)(*hello_message_params)
		connection.send_message(hello_message.serialize())
	# Receives configuration message from server		
	def ReceiveConfigMessage(connection):
		config_message = protocol.get_message(ProtocolMessagesTyeps.CONFIG_MESSAGE).read(connection.receive_message())
		return config_message
	# Sends snapshot message to server
	def SendSnapshotMessage(connection, snapshot, fields):
		snapshot_message = protocol.get_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE)(snapshot, fields)
		connection.send_message(snapshot_message.serialize())
	# Reading mind file according to it's version and sending it to server
	with MindFileReader(file_path, version) as sample_reader:
		with Connection.connect(server_ip_str, server_port_int) as connection:					
			# Sending hello message
			user_information = sample_reader.user_information
			SendHelloMessage(connection, user_information)
			# Receiving configuration message
			config_message = ReceiveConfigMessage(connection)
			fields = config_message.fields			
			# Sending snapshot messages
			for snapshot in sample_reader:
				SendSnapshotMessage(connection, snapshot, fields)
	logger.info(UPLOAD_SAMPLE_FILE_HAS_FINISHED_INFO_MESSAGE)
