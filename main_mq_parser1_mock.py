from pathlib import Path

from cortex.publisher_consumer.message_queue import MessageQueuePublisher
from cortex.publisher_consumer.message_queue import MessageQueueConsumer 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

def get_filename(fpath):
    return Path(fpath).stem

def get_parser_number(s):
    return [c for c in s if c.isdigit()][0]

class Parser:
    def __init__(self):
        self.parser_number 	= get_parser_number(get_filename(__file__))
        self.parser_name 	= 'parser.' + self.parser_number
        
    # Generates parse callback with custom arguments - by this currying function 
    def generate_callback(self):
        def parse(message):
            print(f'{self.parser_name} Received {message}')
            message = str(message).replace('Server', self.parser_name)
            self.publish_function(message, routing_key=self.parser_name)
        return parse
    
    def run(self):
        self.register_publish()
        self.listen()
    
    def listen(self):
        mq_context_factory      = MessageQueueContextFactory()
        message_queue_context   = mq_context_factory.get_mq_context('parser', 'consumers', 'snapshots') 
        message_queue_consumer  = MessageQueueConsumer(self.generate_callback(), message_queue_context)
        message_queue_consumer.run()
    
    def register_publish(self):
        mq_context_factory      = MessageQueueContextFactory()
        message_queue_context   = mq_context_factory.get_mq_context('parser', 'publishers', 'parsed_snapshot', name=self.parser_name)
        message_queue_publisher = MessageQueuePublisher(message_queue_context)
        self.publish_function   = message_queue_publisher.run()
        
if "__main__" == __name__:
    parser = Parser()
    parser.run()
    