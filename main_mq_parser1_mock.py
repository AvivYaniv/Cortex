from pathlib import Path

from cortex.publisher_consumer.message_queue import MessageQueueContext
from cortex.publisher_consumer.message_queue import MessageQueuePublisher
from cortex.publisher_consumer.message_queue import MessageQueueConsumer 

def get_filename(fpath):
    return Path(fpath).stem

def get_parser_number(str):
    return [s for s in str if s.isdigit()][0]

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
        message_queue_context =             \
        MessageQueueContext(                \
            exchange_type  = 'fanout',      \
            exchange_name  = 'raw',         \
            queue_name     = '',            \
            binding_keys   = [ 'snapshot' ] \
            )    
        message_queue_consumer = MessageQueueConsumer(self.generate_callback(), message_queue_context)
        message_queue_consumer.run()
    
    def register_publish(self):
        message_queue_context =                 \
        MessageQueueContext(                    \
            exchange_type  = 'fanout',          \
            exchange_name  = self.parser_name,  \
            queue_name     = '',                \
            binding_keys   = None               \
            )
        message_queue_publisher = MessageQueuePublisher(message_queue_context)
        self.publish_function   = message_queue_publisher.run()
        
if "__main__" == __name__:
    parser = Parser()
    parser.run()
    