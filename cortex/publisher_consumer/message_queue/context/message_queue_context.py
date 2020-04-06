
class MessageQueueRole:
    TX    =    0
    RX    =    1

class MessageQueueContext:
    def __init__(self, exchange_type, exchange_name='', queue_name='', binding_keys=None):
        self.exchange_type  = exchange_type
        self.exchange_name  = exchange_name
        self.queue_name     = queue_name
        self.binding_keys    = binding_keys
        
    def set_reciver(self):
        self.role = MessageQueueRole.RX
        
    def set_transmitter(self):
        self.role = MessageQueueRole.TX
        
    def is_reciver(self):
        return MessageQueueRole.RX == self.role
    
    def is_transmitter(self):
        return MessageQueueRole.TX == self.role
        