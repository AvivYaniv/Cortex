from struct import pack, calcsize

from ..utils import Serialization

class ConfigMessage:
    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER        = 'I'
    SERIALIZATION_FIELD_HEADER  = 'I'
    SERIALIZATION_FIELD_PAYLOAD = '{0}s'
    
    def __init__(self, *args):
        self.fields_number  = len(args)
        self.fields         = args
         
    def __repr__(self):
        return f'ConfigMessage(fields_number={self.fields_number}, fields={self.fields})'
    
    def __str__(self):
        return f'Fields={self.fields}'
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):        
            # fields_number  :    uint32
            # <list> :            
            #     field_size :    uint32
            #     field      :    char[]
            self._current_serialization_format = ConfigMessage.SERIALIZATION_ENDIANITY + ConfigMessage.SERIALIZATION_HEADER
            for field_index in range(self.fields_number):
                field=self.fields[field_index]
                self._current_serialization_format += ConfigMessage.SERIALIZATION_FIELD_HEADER
                self._current_serialization_format += ConfigMessage.SERIALIZATION_FIELD_PAYLOAD.format(len(field))
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
            field=self.fields[field_index]
            args_list.append(len(field))
            args_list.append(field)
        return pack(args_list)
    
    @staticmethod
    def deserialize(*, stream):
        fields_number                                       = \
            Serialization.deserialize(stream, ConfigMessage.SERIALIZATION_HEADER)
        
        fields = []
        
        for field_index in range(fields_number):
            field_size                                      = \
                Serialization.deserialize(stream, ConfigMessage.SERIALIZATION_FIELD_HEADER)
            FIELD_PAYLOAD_FORMAT                            = ConfigMessage.SERIALIZATION_FIELD_PAYLOAD.format(field_size)
            field                                           = \
                Serialization.deserialize(stream, FIELD_PAYLOAD_FORMAT)
            fields.append(field)
        
        return ConfigMessage(*fields)
    
    