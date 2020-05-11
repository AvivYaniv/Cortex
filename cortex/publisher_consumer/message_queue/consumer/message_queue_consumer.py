
from cortex.publisher_consumer.message_queue.message_queue_runner import get_message_queue 

class MessageQueueConsumer:
    def __init__(self, 
                 callback,
                 message_queue_context,
                 message_queue_type =   None,
                 host               =   None,
                 port               =   None):
        self.callback                    =   callback
        self.message_queue_context       =   message_queue_context
        self.message_queue_type          =   message_queue_type
        self.host                        =   host
        self.port                        =   port
        self.message_queue_context.set_reciver()
        self.message_queue               =   get_message_queue(message_queue_context  =   self.message_queue_context,
                                                               callback               =   self.callback,
                                                               message_queue_type     =   self.message_queue_type,
                                                               host                   =   self.host,
                                                               port                   =   self.port)
    
    def run(self):
        self.message_queue.run()
    