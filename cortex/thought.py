import time
from struct import pack, unpack, calcsize
from datetime import datetime

class Thought:
    ERROR_DATA_INCOMPLETE           = 'incomplete data'
    
    DATETIME_FORMAT                 = '%Y-%m-%d_%H:%M:%S'
    
    THOUGHT_HEADER_FORMAT           = '<QQI'
    HEADER_SIZE                     = calcsize(THOUGHT_HEADER_FORMAT)
    
    def __init__(self, user_id, timestamp, thought):
        self.user_id    = int(user_id)
        self.timestamp  = timestamp
        self.thought    = thought
        
    def __repr__(self):
        return f'Thought(user_id={self.user_id}, timestamp={self.timestamp.__repr__()}, thought=\"{self.thought}\")'

    def __str__(self):
        return f'[{datetime.strftime(self.timestamp, Thought.DATETIME_FORMAT)}] user {self.user_id}: {self.thought}'
    
    def __eq__(self, other):
        if isinstance(other, Thought):
            return                                           \
                (self.user_id   ==  other.user_id)       and \
                (self.timestamp ==  other.timestamp)     and \
                (self.thought   ==  other.thought)
        return False
    
    def serialize(self):
        thought_size, thought_data      = len(self.thought), self.thought.encode('utf-8')
                
        # user_id        :    uint64
        # timestamp      :    uint64
        # thought_size   :    uint32
        # thought_data   :    <thought size> bytes
        THOUGHT_DATA_FORMAT             = '{0}s'.format(thought_size)
        THOUGHT_FORMAT                  = Thought.THOUGHT_HEADER_FORMAT + THOUGHT_DATA_FORMAT
        
        time_stamp_as_number = int(time.mktime(self.timestamp.timetuple()))
        
        return                          \
            pack(THOUGHT_FORMAT,        \
                 self.user_id,          \
                 time_stamp_as_number,  \
                 thought_size,          \
                 thought_data)
    
    @staticmethod
    def parse_thought_header(thought_header):
        # If data isn't enough to contain header
        if (Thought.HEADER_SIZE > len(thought_header)):
            raise RuntimeError(Thought.ERROR_DATA_INCOMPLETE)
        
        # Parsing the data header
        user_id_number, timestamp, thought_size = \
            unpack(Thought.THOUGHT_HEADER_FORMAT, thought_header[:Thought.HEADER_SIZE])
                
        # Parsing datetime
        datetime_parsed              = datetime.fromtimestamp(timestamp)
        
        # Return parsed thought
        return (datetime_parsed, user_id_number, thought_size)
    
    @staticmethod
    def parse_thought_data(thought_data):
        # Parsing thought data
        THOUGHT_DATA_FORMAT             = '<{0}s'.format(len(thought_data))
        parsed_thought_data             = unpack(THOUGHT_DATA_FORMAT, thought_data)[0].decode("utf-8")
        
        return parsed_thought_data
    
    @staticmethod
    def deserialize(data):
        thought_header                                      = data[:Thought.HEADER_SIZE]
        raw_thought_data                                    = data[Thought.HEADER_SIZE:]
        
        (datetime_parsed, user_id_number, thought_size)     = Thought.parse_thought_header(thought_header)

        parsed_thought_data                                 = Thought.parse_thought_data(raw_thought_data)
        
        return Thought(user_id_number, datetime_parsed, parsed_thought_data)
    