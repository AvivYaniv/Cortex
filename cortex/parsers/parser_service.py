from cortex.publisher_consumer.message_queue import MessageQueuePublisher
from cortex.publisher_consumer.message_queue import MessageQueueConsumer 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

from cortex.parsers.snapshot import Parser

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
ERROR_DURING_INITIALIZATION_CANT_RUN_ERROR_MESSAGE  =   'Parser service initialization failed, can\'t run'

class ParserService:
    SERVICE_TYPE        =   'parser'
    
    @staticmethod 
    def get_parser_name(parser_type):
        return f'parser.{parser_type}'
    
    def __init__(self, parser_type, message_queue_type, message_queue_host, message_queue_port):
        self.initialized        = True
        self.parser_type        = parser_type
        self.parser_name        = ParserService.get_parser_name(parser_type)
        self.message_queue_type = message_queue_type
        self.message_queue_host = message_queue_host
        self.message_queue_port = message_queue_port
        self.parser             = Parser(parser_type)
        self.initialized        = self.parser.initialized
        
    # Generates parse callback with custom arguments - by this currying function 
    def publish_parsed_callback(self):
        def parse_and_publish(message):
            logger.info(f'{self.parser_name} Received {message}')
            # context = self.get_context(message)
            context = None
            # TODO GENERATE CONTEXT
            parsed  = self.parser.parse(context, message)
            self.publish_function(parsed, publisher_name=self.parser_name)
            logger.info(f'{self.parser_name} Parsed {parsed}')
        return parse_and_publish
    
    def run(self):
        if not self.initialized:
            logger.error(ERROR_DURING_INITIALIZATION_CANT_RUN_ERROR_MESSAGE)
            return
        mq_context_factory      =   MessageQueueContextFactory(self.message_queue_type)
        self.register_publish_parsed(mq_context_factory)
        self.consume_messages(mq_context_factory)
    
    def consume_messages(self, mq_context_factory):
        message_queue_context   =                   \
            mq_context_factory.get_mq_context(ParserService.SERVICE_TYPE, 'consumers', 'snapshots') 
        message_queue_consumer  =                   \
            MessageQueueConsumer(                   \
                self.publish_parsed_callback(),     \
                message_queue_context,              \
                self.message_queue_type,            \
                self.message_queue_host,            \
                self.message_queue_port,            \
                )
        message_queue_consumer.run()
    
    def register_publish_parsed(self, mq_context_factory):
        message_queue_context   = \
            mq_context_factory.get_mq_context(ParserService.SERVICE_TYPE, 'publishers', 'parsed_snapshot', name=self.parser_name)
        message_queue_publisher = MessageQueuePublisher(message_queue_context)
        self.publish_function   = message_queue_publisher.run()
        
def run_parser_service(parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None):
    parser = ParserService(parser_type, message_queue_type, message_queue_host, message_queue_port)
    parser.run()
    