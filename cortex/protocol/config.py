class ConfigMessage:
    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'I'
    SERIALIZATION_FIELD     = 'I{0}s'
    SERIALIZATION_FORMAT    = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_PAYLOAD
    
    def __init__(self, *args):
        self.fields_number  = len(args)
        self.fields         = args
         
    def __repr__(self):
        return f'ConfigMessage(fields_number={self.fields_number}, fields={self.username}, birth_date={datetime.strftime(self.birth_date, UserInformation.DATETIME_FORMAT)}, gender={self.gender})'
    
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):        
            username_size = len(self.username)
            
            # user_id        :    uint64
            # username       :    uint32 + string of <username_size> length
            # birth_date     :    uint32
            # gender         :    char
            self._current_serialization_format = UserInformation.SERIALIZATION_FORMAT.format(username_size)
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        username_size                   = len(self.username)
        birth_date_as_number            = int(time.mktime(self.birth_date.timetuple()))
       
        return                                              \
            pack(self.get_current_serialization_format(),   \
                 self.user_id,                              \
                 username_size,                                 \
                 self.username,                                 \
                 birth_date_as_number,                      \
                 self.gender)
    
    @staticmethod
    def deserialize(*, stream):
        header_size                                    = calcsize(UserInformation.SERIALIZATION_HEADER)
        data_header                                    = stream.read(header_size)
        
        if data_header is None:
            raise RuntimeError(UserInformation.ERROR_DATA_INCOMPLETE)
        
        user_id, username_size = \
            unpack(UserInformation.SERIALIZATION_HEADER, data_header)
        
        CURRENT_USER_PAYLOAD_FORMAT                    = (UserInformation.SERIALIZATION_ENDIANITY + UserInformation.SERIALIZATION_PAYLOAD).format(username_size)
        
        payload_size                                   = calcsize(CURRENT_USER_PAYLOAD_FORMAT)
        data_payload                                   = stream.read(payload_size)        
        
        if data_payload is None:
            raise RuntimeError(UserInformation.ERROR_DATA_INCOMPLETE)
        
        username, birth_date, gender                   = unpack(CURRENT_USER_PAYLOAD_FORMAT, data_payload)
        
        return UserInformation(user_id, username, datetime.fromtimestamp(birth_date), gender)
    