import threading

from cortex.publisher_consumer.message_queue.consumer import MessageQueueConsumer 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

class MessageQueueConsumerThread(threading.Thread):
    def __init__(self, callback, caller_type, category, item, message_queue_type = None, host = None, **kwargs):
            threading.Thread.__init__(self)
            mq_context_factory          =   MessageQueueContextFactory(message_queue_type)
            message_queue_context       =   mq_context_factory.get_mq_context(caller_type, category, item, **kwargs)
            self.message_queue_consumer =   MessageQueueConsumer(callback, message_queue_context, message_queue_type, host)
        
    def run(self):        
        self.message_queue_consumer.run()
        