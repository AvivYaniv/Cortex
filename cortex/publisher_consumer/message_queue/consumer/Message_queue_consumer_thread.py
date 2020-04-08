import threading

from cortex.publisher_consumer.message_queue.consumer import MessageQueueConsumer 

class MessageQueueConsumerThread(threading.Thread):
    def __init__(self, callback, message_queue_context, message_queue_type = None, host = None, port = None):
            threading.Thread.__init__(self)
            self.message_queue_consumer =   MessageQueueConsumer(callback, message_queue_context, message_queue_type, host, port)
        
    def run(self):        
        self.message_queue_consumer.run()
        