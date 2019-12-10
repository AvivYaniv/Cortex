from struct import pack, unpack, calcsize

class Serialization:
    ERROR_DATA_INCOMPLETE   = 'incomplete data'
    
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
    