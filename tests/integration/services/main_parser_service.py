
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.parsers import run_parser_service

if "__main__" == __name__:
    parser_type = 'user_feeling'
    parser_service = run_parser_service(parser_type, message_queue_type=None, message_queue_host=None, message_queue_port=None)
    parser_service.run()
