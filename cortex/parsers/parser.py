
from cortex.utils.url import parse_url

from cortex.parsers.parser_service import run_parser_service

def run_parser(parser_type, mq_url=None):
    """Starts a parser of the given type and publishes parsed output to message-queue"""  
    message_queue_type, message_queue_host, message_queue_port  =   \
        parse_url(mq_url)
    parser_service = run_parser_service(parser_type, message_queue_type, message_queue_host, message_queue_port)
    parser_service.run()
