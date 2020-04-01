from struct import pack, unpack, calcsize
from numpy.lib import stride_tricks

class Serialization:
    ERROR_DATA_INCOMPLETE   = 'incomplete data'
    
    TUNNLE_MESSAGE_HEADER           = 'I'
    TUNNLE_MESSAGE_PAYLOAD_FORMAT   = '{0}s'
    TUNNLE_MESSAGE_FORMAT           = TUNNLE_MESSAGE_HEADER + TUNNLE_MESSAGE_PAYLOAD_FORMAT
    
    @staticmethod
    def serialize_tunnled_message(data, endianity = '<'):
        size = len(data)
        return pack(endianity + Serialization.TUNNLE_MESSAGE_FORMAT.format(size),
                    size,
                    data)
    
    @staticmethod
    def read_tunnled_message(stream, endianity = '<'):
        message_size = Serialization.read(stream, Serialization.TUNNLE_MESSAGE_HEADER, endianity = '<', expect_eof=True)[0]
        return stream.read(message_size)
    
    @staticmethod
    def remove_endianity(data):
        if (0 == len(data)):
            return data
        e = data[0]
        if e not in ['<', '>', '!', '@', '=']:
            return data
        return data[1:] 
    
    @staticmethod
    def deserialize(arr, serialization_format, offset, endianity = '<', expect_eof = False):
        serialization_size   =   calcsize(endianity + serialization_format)        
        if (len(arr) - offset) < serialization_size:
            if expect_eof:
                raise EOFError()
            else:
                raise RuntimeError(Serialization.ERROR_DATA_INCOMPLETE)
        serialized          =   arr[offset:serialization_size+offset]
        return unpack(endianity + serialization_format, serialized)
    
    @staticmethod
    def read(stream, serialization_format, endianity = '<', expect_eof = False):
        serialization_size  =   calcsize(endianity + serialization_format)        
        serialized          =   stream.read(serialization_size)            
        if not serialized:
            if expect_eof:
                raise EOFError()
            else:
                raise RuntimeError(Serialization.ERROR_DATA_INCOMPLETE)
        return unpack(endianity + serialization_format, serialized)
    