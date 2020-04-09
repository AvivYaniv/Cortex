from struct import pack, unpack, calcsize
import socket

import time

class Connection:
    NOT_ALL_DATA_RECEIVED_ERROR  =   'Error! not all data received'
    
    SERIALIZATION_ENDIANITY      = '<'

    SERIALIZATION_HEADER         = 'I'
    SERIALIZATION_PAYLOAD        = '{0}s'
    SERIALIZATION_FORMAT         = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_PAYLOAD
    
    CONNECTION_RETRIES_NUMBER    = 20
    CONNECTION_RETRY_DELAY       = 3
    
    def __init__(self, sock):
        self.sock = sock

    def __enter__(self):
        return self
    
    def __exit__(self, exception, error, traceback):
        self.close()
        if exception is not EOFError:
            print(str(exception))
            raise exception
        return True
    
    def __repr__(self):
        local_ip, local_port = self.sock.getsockname()
        other_ip, other_port = self.sock.getpeername()
        return f'<Connection from {local_ip}:{local_port} to {other_ip}:{other_port}>'

    @classmethod
    def connect(cls, host, port):
        server_ip_str                   = host
        server_port_int                 = int(port)
                
        # Connect to server
        sock = socket.socket()
        
        for retry_number in range(Connection.CONNECTION_RETRIES_NUMBER):
            try:
                sock.connect((server_ip_str, server_port_int))
                break
            except ConnectionRefusedError as e:
                print(e)
                time.sleep(Connection.CONNECTION_RETRY_DELAY)        
        return cls(sock)
        
    def send(self, data):
        self.sock.sendall(data)
        
        
    def receive(self, size):
        from_client = b''
        remaining_to_recive = size    
        while 0 < remaining_to_recive:
             data = self.sock.recv(remaining_to_recive)
             if not data: break             
             from_client += data
             remaining_to_recive -= len(data)  
        if 0 < remaining_to_recive:
            raise RuntimeError(Connection.NOT_ALL_DATA_RECEIVED_ERROR)
        return from_client 
    
    def close(self):
        self.sock.close()
        
    def send_message(self, data):
        if not data:
            return
        message_size     = len(data)                
        message =                                                       \
            pack(Connection.SERIALIZATION_FORMAT.format(message_size),  \
                 message_size,                                          \
                 data)            
        self.send(message)

    
    def receive_message(self):
        header_size                             = calcsize(Connection.SERIALIZATION_HEADER)
        data_header                             = self.sock.recv(header_size)
        
        if data_header is None or 0 == len(data_header):
            raise EOFError(Connection.NOT_ALL_DATA_RECEIVED_ERROR)
        
        message_size                            = \
            unpack(Connection.SERIALIZATION_HEADER, data_header)[0]

        return self.receive(message_size)
        