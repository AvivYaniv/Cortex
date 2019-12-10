from pathlib import Path, PurePath

from .utils import Connection

from .protocol import HelloMessage, ConfigMessage, SnapshotMessage

from .sample import Snapshot

from .utils import Listener

import threading
        
SUPPORTED_FIELDS = ['datetime', 'translation', 'color_image']
        
class FilesHandler:
    @staticmethod
    def toSafePath(path_name):
        return path_name.replace(':', '-').replace(' ', '_')
    
    @staticmethod
    def write_file(lock, file_path, data_line, mode='a+'):        
        lock.acquire()
        try:
            file_existed = Path(file_path).is_file()
            with open(file_path, mode) as file:                             
                if file_existed:
                    file.write('\n')                
                file.write(data_line)
                file.flush()   
                file.close()             
        finally:            
            lock.release()
        
    @staticmethod
    def write_user_translation(lock, data_dir, user_id, datetime_formatted, translation):
        user_dir                = str(user_id)
        translation_file        = FilesHandler.toSafePath(datetime_formatted) + '.json'
        translation_file_dir    = PurePath(data_dir, user_dir)
        Path(translation_file_dir).mkdir(parents=True, exist_ok=True)
        translation_file_path   = PurePath(translation_file_dir, translation_file)
        FilesHandler.write_file(lock, translation_file_path, '"x": {0}, "y": {1}, "z": {2}'.format(*translation))
        
class Handler(threading.Thread):
    lock       = threading.Lock()
    def __init__(self, connection, data_dir):    
        super().__init__()
        self.connection = connection    
        self.data_dir   = data_dir
    
    def run(self): # start invokes run  		
        # Receive hello message
        hello_message = HelloMessage.read(self.connection.receive_message())
        # Send config message
        config_message = ConfigMessage(*SUPPORTED_FIELDS) 
        self.connection.send_message(config_message.serialize())
        # Receive snapshot messeges
        while True:
            try:
                snapshot_message = SnapshotMessage.read(self.connection.receive_message())                
                FilesHandler.write_user_translation(                                    \
                                                    self.lock,                          \
                                                    self.data_dir,                      \
                                                    hello_message.user_id,              \
                                                    snapshot_message.getTimeStamp(),    \
                                                    snapshot_message.translation)
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
            