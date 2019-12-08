import time
from .thought import *
from .utils import Connection
import socket

def upload_thought(address, user_id, thought):
	"""Sends to the server user's thought"""
	# Parse server address
	server_ip_str, server_port_str  = address.split(":")
	server_port_int                 = int(server_port_str)
	
	thought_object                  = Thought(user_id, datetime.fromtimestamp(int(time.time())), thought)
	
	# Pack Cortex
	packed_thought = thought_object.serialize()
	
	# Connect and sent to server
	sock = socket.socket()
	sock.connect((server_ip_str, server_port_int))
	conn = Connection(sock)
	conn.send(packed_thought)
	
	# Print done
	print('done')
