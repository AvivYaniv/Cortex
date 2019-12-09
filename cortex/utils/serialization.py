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
    def deserialize(stream, serialization_format, endianity = '<', expect_eof = False):
        data_size                                           =   calcsize(endianity + serialization_format)
        data                                                =   stream.read(data_size)
        
        if not data:
            if expect_eof:
                raise EOFError()
            else:
                raise RuntimeError(Serialization.ERROR_DATA_INCOMPLETE)
         
        return unpack(endianity + serialization_format, data)
    