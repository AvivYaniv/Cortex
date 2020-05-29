from cortex.parsers.parser_service import ParserService

from cortex.utils import _FileHandler

class MessageParser:
    def __init__(self, parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        self.parser_service = ParserService(parser_type, message_queue_type, message_queue_host, message_queue_port)
        
    def parse_message_data(self, message_data):
        return self.parser_service.parse_message(message_data).serialize()
    
    def parse_message(self, message_path):
        result, message = _FileHandler.safe_read_file(message_path)
        if not result:
            return message
        return self.parse_message_data(message)
    
def run_parser(parser_type, message_data):
    message_parser = MessageParser(parser_type)
    return message_parser.parse_message_data(message_data)

    