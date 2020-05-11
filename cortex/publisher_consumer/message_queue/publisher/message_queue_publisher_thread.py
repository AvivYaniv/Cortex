import threading

from cortex.publisher_consumer.message_queue.publisher.message_queue_publisher import MessageQueuePublisher

class MessageQueuePublisherThread(threading.Thread):
    def __init__(self, message_queue_context, message_queue_type = None, host = None, port = None):
            threading.Thread.__init__(self)
            self.message_queue_publisher =   MessageQueuePublisher(message_queue_context, message_queue_type, host, port)
        
    def get_publish_function(self):
        return self.message_queue_publisher.get_publish_function()
        
    def run(self):
        self.message_queue_publisher.run()
    