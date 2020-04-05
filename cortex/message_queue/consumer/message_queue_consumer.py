from .consumer import Consumer
from cortex.message_queue.rabbitmq_mq import RabbitMQMessageQueue

from cortex.message_queue.message_queue_runner import run_message_queue 

class MessageQueueConsumer(Consumer):
    def __init__(self, 
                 callback,
                 message_queue_context,
                 message_queue_type     =   RabbitMQMessageQueue.name,
                 host                   =   'localhost'):
        super(MessageQueueConsumer, self).__init__(callback)
        self.callback                    =   callback
        self.message_queue_context       =   message_queue_context
        self.message_queue_type          =   message_queue_type
        self.host                        =   host
        message_queue_context.set_reciver()
        
    def run(self):
        run_message_queue(message_queue_context	 =	 self.message_queue_context,
						  callback				 =	 self.callback,
                          message_queue_type     =   self.message_queue_type,
                          host                   =   self.host)
    