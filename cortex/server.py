from pathlib import Path, PurePath

from .utils import Connection

from .protocol import HelloMessage, ConfigMessage, SnapshotMessage

from .sample import Snapshot

from .utils import Listener

from functools import wraps
import threading
from builtins import staticmethod
        
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
        finally:            
            lock.release()
        
    @staticmethod
    def write_user_translation(lock, path, translation_formatted):
        translation_file        = 'translation.json'
        translation_file_path   = PurePath(path, translation_file)        
        FilesHandler.write_file(lock, translation_file_path, translation_formatted)
    
    @staticmethod
    def write_color_image(lock, path, color_image):
        color_image_file        = 'color_image.jpg'
        color_image_file_path   = str(PurePath(path, color_image_file))
        lock.acquire()
        try:
            color_image.save_image(color_image_file_path)
        finally:            
            lock.release()
    
SUPPORTED_FIELDS = [ 'datetime', 'translation', 'color_image' ]
    
def parser(field):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped_function
    return decorator

@parser('translation')
def parse_translation(context):
    translation_formatted = '{' + '"x": {0}, "y": {1}, "z": {2}'.format(*context.snapshot.translation) + '}'
    FilesHandler.write_user_translation(                        \
                                        context.lock,           \
                                        context.path,           \
                                        translation_formatted)
    

@parser('color_image')
def parse_color_image(context):
    FilesHandler.write_color_image(                             \
                                    context.lock,               \
                                    context.path,               \
                                    context.snapshot.color_image) 
    
class Handler(threading.Thread):
    lock       = threading.Lock()    
    def __init__(self, connection, data_dir):    
        super().__init__()
        self.connection = connection    
        self.data_dir   = data_dir
    
    def get_context(self, hello_message, snapshot_message):
        class Context:
            def __init__(self, lock, path, snapshot):
                self.lock       = lock
                self.path       = path
                self.snapshot   = snapshot
        lock        =   self.lock        
        user_dir    =   str(hello_message.user_id)        
        pure_path   =   PurePath(self.data_dir, user_dir, FilesHandler.toSafePath(snapshot_message.getTimeStamp()))       
        path        =   str(pure_path)
        Path(pure_path).mkdir(parents=True, exist_ok=True)
        snapshot    =   snapshot_message
        return Context(lock, path, snapshot)
    
    def run(self): # start invokes run	
        # Receive hello message        
        hello_message = HelloMessage.read(self.connection.receive_message())
        # Send config message
        config_message = ConfigMessage(*SUPPORTED_FIELDS) 
        self.connection.send_message(config_message.serialize())
        # Receive snapshot messeges
        while True:
            try:
                snapshot_message    =   SnapshotMessage.read(self.connection.receive_message())
                context             =   self.get_context(hello_message, snapshot_message)
                parse_translation(context)
                parse_color_image(context)
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
            