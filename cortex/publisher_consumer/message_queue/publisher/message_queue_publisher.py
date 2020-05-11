
from cortex.publisher_consumer.message_queue.message_queue_runner import get_message_queue 

class MessageQueuePublisher:
    def __init__(self, 
                 message_queue_context,
                 message_queue_type	= None,
                 host               = None,
				 port				= None):
        self.message_queue_context       =   message_queue_context
        self.message_queue_type          =   message_queue_type
        self.host                        =   host
        self.port                        =   port
        self.message_queue_context.set_transmitter()
        self.message_queue               =   get_message_queue(message_queue_context  =   self.message_queue_context,
                                                               message_queue_type     =   self.message_queue_type,
                                                               host                   =   self.host,
                                                               port                   =   self.port)
        
    def get_publish_function(self):
        return self.message_queue.get_publish_function()
    
    def run(self):
        self.message_queue.run() 
    