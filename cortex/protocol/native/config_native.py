import io

from struct import pack, calcsize

from cortex.protocol.config_message import ConfigMessage

from cortex.utils import Serialization

class ConfigMessageNative(ConfigMessage):
    ENCODING                    = 'utf-8'
    
    SERIALIZATION_ENDIANITY     = '<'

    SERIALIZATION_HEADER        = 'I'
    SERIALIZATION_FIELD_HEADER  = 'I'
    SERIALIZATION_FIELD_PAYLOAD = '{0}s'
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):        
            # fields_number  :    uint32
            # <list> :            
            #     field_size :    uint32
            #     field      :    char[]
            self._current_serialization_format = ConfigMessageNative.SERIALIZATION_ENDIANITY + ConfigMessageNative.SERIALIZATION_HEADER
            for field_index in range(self.fields_number):
                field=self.fields[field_index]
                self._current_serialization_format += ConfigMessageNative.SERIALIZATION_FIELD_HEADER
                self._current_serialization_format += ConfigMessageNative.SERIALIZATION_FIELD_PAYLOAD.format(len(field))
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        args_list = []
        args_list.append(self.get_current_serialization_format())
        args_list.append(self.fields_number)
        for field_index in range(self.fields_number):
            field=self.fields[field_index].encode(ConfigMessageNative.ENCODING)
            args_list.append(len(field))
            args_list.append(field)
        return pack(*args_list)
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        return ConfigMessageNative.read_stream(stream)
    
    @staticmethod
    def read_stream(stream):       
        fields_number                                       = \
            Serialization.read(stream, ConfigMessageNative.SERIALIZATION_HEADER)[0]        
        fields_config = []        
        for field_index in range(fields_number):
            field_size                                      = \
                Serialization.read(stream, ConfigMessageNative.SERIALIZATION_FIELD_HEADER)[0]
            FIELD_PAYLOAD_FORMAT                            = ConfigMessageNative.SERIALIZATION_FIELD_PAYLOAD.format(field_size)
            field                                           = \
                Serialization.read(stream, FIELD_PAYLOAD_FORMAT)[0]
            fields_config.append(field.decode(ConfigMessageNative.ENCODING))        
        return ConfigMessage(fields_config)
    
    