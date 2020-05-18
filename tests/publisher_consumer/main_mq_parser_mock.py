
from cortex.publisher_consumer.message_queue import MessageQueuePublisherThread
from cortex.publisher_consumer.message_queue import MessageQueueConsumerThread 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

from tests.test_constants import PARSER_TYPES

from tests.test_constants import MESSAGE_QUEUE_TEST_HOST

from tests.test_constants import PARSER_SERVICE_TYPE

from tests.test_constants import get_message_queue_messages_file_path

from tests._utils.dictionary_file import DictionaryFile

class Parser:
    def __init__(self, parset_type):  
        self.parset_type            = parset_type 
        self.service_type           = PARSER_SERVICE_TYPE
        self.parser_name            = self.parset_type + '.' + self.service_type 
        self.parser_dictionay_file  = DictionaryFile(get_message_queue_messages_file_path(self.service_type))
    
    # Generates callback with custom arguments - by this currying function 
    def publish_parsed_callback(self):
        def parse(message):
            message = message.decode("utf-8")
            self.parser_dictionay_file.append_line(self.parset_type, message)
            self.publish_function(f'[\"{self.parset_type}\", \"{message}\"]', publisher_name=self.parser_name)
        return parse
    
    def run(self):
        self.register_publish_parsed()
        self.consume_messages()
    
    def consume_messages(self):
        mq_context_factory      = MessageQueueContextFactory()
        message_queue_context   = mq_context_factory.get_mq_context('parser', 'consumers', 'snapshots') 
        message_queue_consumer  = MessageQueueConsumerThread(self.publish_parsed_callback(), message_queue_context, host=MESSAGE_QUEUE_TEST_HOST)
        message_queue_consumer.run()
    
    def register_publish_parsed(self):
        mq_context_factory      = MessageQueueContextFactory()
        message_queue_context   = mq_context_factory.get_mq_context('parser', 'publishers', 'parsed_snapshot', name=self.parser_name)
        message_queue_publisher = MessageQueuePublisherThread(message_queue_context, host=MESSAGE_QUEUE_TEST_HOST)
        self.publish_function   = message_queue_publisher.get_publish_function()
        message_queue_publisher.run()

        
def run_parser_mock(parser_type=None):
    parser_type = parser_type if parser_type else PARSER_TYPES[0]
    parser = Parser(parser_type)
    parser.run()
    
if "__main__" == __name__:
    run_parser_mock()
