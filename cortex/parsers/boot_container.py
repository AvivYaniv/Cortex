
from cortex.envvars import get_message_queue_parameters

from cortex.parsers.parser_service import run_parser_service

import os
import sys

# Constants Section
PARSER_TYPE_ENVIRONMENT_VARIABLE                    =   'PARSER'

# Messages Section
PARSER_TYPE_NOT_CONFIGURED_ERROR_MESSAGE            =   'Parser type not configured in container'

def run_parser(parser_type, message_queue_type, message_queue_host, message_queue_port):
    run_parser_service(parser_type, message_queue_type, message_queue_host, message_queue_port)

if "__main__" == __name__:
    if PARSER_TYPE_ENVIRONMENT_VARIABLE not in os.environ:
        print(PARSER_TYPE_NOT_CONFIGURED_ERROR_MESSAGE)
        sys.exit()
    parser_type                     = os.environ[PARSER_TYPE_ENVIRONMENT_VARIABLE]
    message_queue_type, host, port  = get_message_queue_parameters()
    run_parser(parser_type, message_queue_type, host, port)
    