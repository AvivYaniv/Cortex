import socket

from cortex.utils.network.connection import Connection

class Listener:
    DEFAULT_HOST    = '0.0.0.0'
    DEFAULT_BACKLOG = 1000
    DEFAULT_REUSE   = True
    
    def __init__(self, port, host=DEFAULT_HOST, backlog=DEFAULT_BACKLOG, reuseaddr=DEFAULT_REUSE):
        self.port       = port
        self.host       = host
        self.backlog    = backlog
        self.reuseaddr  = reuseaddr
        
    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'
        
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exception, error, traceback):
        self.stop()
        if exception is not None:
            print('DEBUG ' + str(exception))
            raise exception
        return True
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        
        self.server.bind((self.host, self.port))
        self.server.consume_messages(self.backlog)
    
    def stop(self):
        self.server.close()
    
    def accept(self):
        # Accept client        
        client, _ = self.server.accept()
        return Connection(client)
