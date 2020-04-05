from .publisher import Publisher
from cortex.message_queue.rabbitmq_mq import RabbitMQMessageQueue

from cortex.message_queue.message_queue_runner import run_message_queue 

class MessageQueuePublisher(Publisher):
    def __init__(self, 
                 message_queue_context,
                 message_queue_type	= RabbitMQMessageQueue.name,
                 host             	= 'localhost'):
        self.message_queue_context       =   message_queue_context
        self.message_queue_type          =   message_queue_type
        self.host                        =   host
        message_queue_context.set_transmitter()
        
    def run(self):
        return run_message_queue(message_queue_context  =   self.message_queue_context,
                                 message_queue_type     =   self.message_queue_type,
                                 host                   =   self.host)
    