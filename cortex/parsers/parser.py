
from cortex.utils.url import parse_url

from cortex.parsers.parser_service import ParserService

from cortex.parsers.parser_service import run_parser_service

from cortex.utils import _FileHandler

class MessageParser:
    def __init__(self, parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        self.parser_service = ParserService(parser_type, message_queue_type, message_queue_host, message_queue_port)
    
    def parse_message(self, message_path):
        result, message = _FileHandler.safe_read_file(message_path)
        if not result:
            return message
        return self.parser_service.parse_message(message)

def run_parser(parser_type, mq_url=None):
    """Starts a parser of the given type and publishes parsed output to message-queue"""  
    message_queue_type, message_queue_host, message_queue_port  =   \
        parse_url(mq_url)
    parser_service = run_parser_service(parser_type, message_queue_type, message_queue_host, message_queue_port)
    parser_service.run()
