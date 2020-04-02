from pathlib import Path, PurePath

from cortex.utils import Connection

from cortex.parsers import Parser

from cortex.protocol import MessagesTyeps, Protocol, snapshot_message

from cortex.sample import Snapshot

from cortex.utils import Listener

from functools import wraps
import threading
from builtins import staticmethod

import logging
from cortex.logger import LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = LoggerLoader()
logger_loader.load_log_config()
        
class FilesHandler:
    @staticmethod
    def toSafePath(path_name):
        return path_name.replace(':', '-').replace(' ', '_')
            
    @staticmethod
    def save(lock, file_path, data, mode='a+'):
        lock.acquire()
        try:
            with open(file_path, mode) as file:                             
                file.write(data)
        finally:            
            lock.release()
    
class Handler(threading.Thread):
    lock       = threading.Lock()    
    def __init__(self, connection, data_dir):    
        super().__init__()
        self.connection             = connection    
        self.data_dir               = data_dir
        self.parser                 = Parser()
        self.supported_fields       = self.parser.get_fields_names()
        self.protocol               = Protocol()
    
    def get_context(self, hello_message, snapshot_message):
        class Context:
            def __init__(self, lock, path, snapshot):
                self.lock       = lock
                self.pure_path  = path
                self.snapshot   = snapshot
                Path(self.pure_path).mkdir(parents=True, exist_ok=True)
            
            def path(self, file_name):
                return str(self.pure_path / Path(FilesHandler.toSafePath(file_name)))
            
            def save(self, file_name, data):
                FilesHandler.save(self.lock, self.path(file_name), data)
                
        lock        =   self.lock        
        user_dir    =   str(hello_message.user_id)        
        path        =   PurePath(self.data_dir, user_dir, FilesHandler.toSafePath(snapshot_message.getTimeStamp()))       
        snapshot    =   snapshot_message
        return Context(lock, path, snapshot)
    
    def run(self): # start invokes run	
        # Receive hello message        
        hello_message_bytes = self.connection.receive_message()
        hello_message       = self.protocol.get_message(MessagesTyeps.HELLO_MESSAGE).read(hello_message_bytes)
        # Send config message
        config_message = self.protocol.get_message(MessagesTyeps.CONFIG_MESSAGE)(*self.supported_fields)
        self.connection.send_message(config_message.serialize())
        # Receive snapshot messages
        while True:
            try:
                snapshot_message_bytes  =   self.connection.receive_message()
                snapshot_message        =   self.protocol.get_message(MessagesTyeps.SNAPSHOT_MESSAGE).read(snapshot_message_bytes)
                context                 =   self.get_context(hello_message, snapshot_message)
                self.parser.parse(context, snapshot_message)
            except EOFError:            
                break

def run_server(host='127.0.0.1', port='8000', data_dir='data'):
    """Starts a server to which snapshots can be uploaded with `upload_sample`"""  
    logger.info("TODO UPDATE Processing data")
    
    # Parse server address
    server_ip_str, server_port_str  = host, port
    server_port_int                 = int(server_port_str)
    
    with Listener(server_port_int, server_ip_str) as listener:
        # Accept client        
        connection = listener.accept()        
        # Initialize client Handler
        handler = Handler(connection, data_dir)        
        # Handle client
        handler.start()
            