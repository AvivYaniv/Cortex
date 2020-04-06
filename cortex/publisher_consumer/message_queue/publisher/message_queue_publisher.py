
from cortex.publisher_consumer.message_queue.message_queue_runner import run_message_queue 

class MessageQueuePublisher:
    def __init__(self, 
                 message_queue_context,
                 message_queue_type	= None,
                 host               = None):
        self.message_queue_context       =   message_queue_context
        self.message_queue_type          =   message_queue_type
        self.host                        =   host
        
    def run(self):
        return run_message_queue(message_queue_context  =   self.message_queue_context,
                                 message_queue_type     =   self.message_queue_type,
                                 host                   =   self.host)
    