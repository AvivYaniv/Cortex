
from cortex.protocol import ProtocolMessagesTyeps, Protocol
from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

from cortex.publisher_consumer.message_queue import MessageQueuePublisher
from cortex.publisher_consumer.message_queue import MessageQueueConsumer 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

from cortex.parsers.snapshot import Parser

import logging
from cortex.logger import _LoggerLoader
from cortex.utils import _FileHandler

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Messages Section
ERROR_DURING_INITIALIZATION_CANT_RUN_ERROR_MESSAGE  =   'Parser service initialization failed, can\'t run'

class ParserContext:
    def __init__(self, user_info, snapshot_uuid, parser_type):
        self.user_id        = user_info.user_id
        self.user_info      = user_info
        self.snapshot_uuid  = snapshot_uuid
        self.parser_type    = parser_type

class ParserService:
    SERVICE_TYPE        =   'parser'
    
    @staticmethod 
    def get_parser_name(parser_type):
        return f'{parser_type}.parser'
    
    def __init__(self, parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        self.parser_type        = parser_type
        self.parser_name        = ParserService.get_parser_name(parser_type)
        self.parser             = Parser(parser_type)
        self.initialized        = self.parser.initialized
        # Message Queue
        self.message_queue_type = message_queue_type
        self.message_queue_host = message_queue_host
        self.message_queue_port = message_queue_port
        # Messages
        self.protocol           = Protocol() 
        self.messages           = MessageQueueMessages()        
    # Snapshot Methods Section
    def desrialize_raw_snapshot_message(self, incoming_snapshot_message):
        raw_snapshot_message =                                      \
            self.messages.get_message(                              \
                MessageQueueMessagesTyeps.RAW_SNAPSHOT_MESSAGE).deserialize(incoming_snapshot_message)
        return raw_snapshot_message
    def _set_context(self, raw_snapshot_message):
        return ParserContext(raw_snapshot_message.user_info, raw_snapshot_message.snapshot_uuid, self.parser_type)    
    # Reads raw snapshot message
    def read_raw_snapshot(self, raw_snapshot_message):
        raw_snapshot_path       = raw_snapshot_message.raw_snapshot_path
        raw_snapshot            = _FileHandler.read_file(raw_snapshot_path, 'rb')
        snapshot                = \
            self.protocol.get_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE).read(raw_snapshot)
        return snapshot
    # Generates parse callback with custom arguments - by this currying function 
    def publish_parsed_callback(self):
        def parse_and_publish(incoming_snapshot_message):
            logger.info(f'{self.parser_name} Received message')
            try:
                raw_snapshot_message    = self.desrialize_raw_snapshot_message(incoming_snapshot_message)
            except Exception as e:
                logger.error(f'error deserializing raw snapshot message : {e}')
                return
            try:
                snapshot                = self.read_raw_snapshot(raw_snapshot_message)
            except Exception as e:
                logger.error(f'error reading snapshot file {raw_snapshot_message.raw_snapshot_path} : {e}')
                return            
            context                     = self._set_context(raw_snapshot_message)
            is_uri, result              = self.parser.export_parse(context, snapshot)
            parsed_snapshot_message     =                               \
                self.messages.get_message(                              \
                    MessageQueueMessagesTyeps.PARSED_SNAPSHOT_MESSAGE)( \
                        context.user_info,                              \
                        context.snapshot_uuid,                          \
                        self.parser_type,                               \
                        result,                                         \
                        is_uri)
            self.publish_function(parsed_snapshot_message.serialize(), publisher_name=self.parser_name)
            logger.info(f'{self.parser_name} Parsed message')
        return parse_and_publish
    # Core Logic Method Section
    def run(self):
        if not self.initialized:
            logger.error(ERROR_DURING_INITIALIZATION_CANT_RUN_ERROR_MESSAGE)
            return
        mq_context_factory      =   MessageQueueContextFactory(self.message_queue_type)
        self.register_publish_parsed(mq_context_factory)
        self.consume_messages(mq_context_factory)
    # Message Queue Methods Section
    # Consume snapshot messages
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
    # Publish parsed
    def register_publish_parsed(self, mq_context_factory):
        message_queue_context   = \
            mq_context_factory.get_mq_context(ParserService.SERVICE_TYPE, 'publishers', 'parsed_snapshot', name=self.parser_name)
        message_queue_publisher = MessageQueuePublisher(message_queue_context)
        self.publish_function   = message_queue_publisher.run()
        
def run_parser_service(parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None):
    parser = ParserService(parser_type, message_queue_type, message_queue_host, message_queue_port)
    parser.run()
    