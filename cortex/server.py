from pathlib import Path, PurePath

from .utils import Connection

from .protocol import HelloMessage, ConfigMessage, SnapshotMessage

from .sample import Snapshot

from .utils import Listener

import threading
        
SUPPORTED_FIELDS = ['datetime', 'translation', 'rotation', 'color_image', 'depth_image', 'user_feeling']
        
class Handler(threading.Thread):
    lock       = threading.Lock()
    def __init__(self, connection, data_dir):    
        super().__init__()
        self.connection = connection    
        self.data_dir   = data_dir

    def recive_thought_header(self):
        return self.connection.
    
    def write_append_file(self, file_path, data_line):        
        self.lock.acquire()
        try:
            file_existed = Path(file_path).is_file()
            with open(file_path, "a+") as file:                             
                if file_existed:
                    file.write('\n')                
                file.write(data_line)
                file.flush()   
                file.close()             
        finally:            
            self.lock.release()
        
    @staticmethod
    def toSafeFileName(file_name):
        return file_name.replace(":", "-")
        
    def write_user_thought(self, datetime_formatted, user_id_number, thought_data):
        # Creating path
        user_dir        = str(user_id_number)
        thought_file    = Handler.toSafeFileName(datetime_formatted) + '.txt'
        
        thought_file_dir = PurePath(self.data_dir, user_dir)
        
        Path(thought_file_dir).mkdir(parents=True, exist_ok=True)
        
        thought_file_path = PurePath(thought_file_dir, thought_file)
        
        # Write user Cortex
        self.write_append_file(thought_file_path, thought_data)
    
    def run(self): # start invokes run  		
        # Receive hello message
        hello_message = HelloMessage.deserialize(self.connection.receive_message())
        # Send config message
        config_message = ConfigMessage(*SUPPORTED_FIELDS) 
        self.connection.send_message(config_message)
        # Receive snapshot messeges
        while True:
            try:
                snapshot_message = SnapshotMessage.deserialize(self.connection.receive_message())
                # TODO HANDLE
            except EOFError:            
                break

def run_server(address, data_dir='data'):
    """Starts a server to which snapshots can be uploaded with `upload_sample`"""  
	# Parse server address
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    
    with Listener(server_port_int, server_ip_str) as listener:
    	# Accept client        
        connection = listener.accept()        
        # Initialize client Handler
        handler = Handler(connection, data_dir)        
        # Handle client
        handler.start()
        