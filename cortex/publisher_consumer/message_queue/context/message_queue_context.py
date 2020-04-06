
class MessageQueueRole:
    TX    =    0
    RX    =    1

class MessageQueueContext:
    def __init__(self):
        pass
        
    def set_reciver(self):
        self.role = MessageQueueRole.RX
        
    def set_transmitter(self):
        self.role = MessageQueueRole.TX
        
    def is_reciver(self):
        return MessageQueueRole.RX == self.role
    
    def is_transmitter(self):
        return MessageQueueRole.TX == self.role
        