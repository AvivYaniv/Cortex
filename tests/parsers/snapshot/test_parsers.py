
import pytest

from cortex.parsers.parser import MessageParser

from cortex.server.server_service import ServerService
from cortex.parsers.parser_service import ParserService
from cortex.saver.saver_service import SaverService

from tests.test_constants import PARSER_TYPES
from tests.test_constants import get_message_queue_mesages_file_path
from cortex.utils.files.file_handler import _FileHandler

def run_parser_handling_of_server_message_test(parser_type):
    message_parser                          = MessageParser(parser_type)
    parser_input_message_file_path          = get_message_queue_mesages_file_path(  \
                                                ServerService.SERVICE_TYPE,         \
                                                ParserService.SERVICE_TYPE,         \
                                                reciver_identifier=parser_type)
    parser_output_message_actual            = message_parser.parse_message(parser_input_message_file_path)
    parser_output_message_expectd_file_path = get_message_queue_mesages_file_path(  \
                                                ParserService.SERVICE_TYPE,         \
                                                SaverService.SERVICE_TYPE,         \
                                                sender_identifier=parser_type)  
    parser_output_message_expectd           = _FileHandler.read_file(parser_output_message_expectd_file_path)
    assert parser_output_message_expectd == parser_output_message_actual, f'Parser {parser_type} output message mismatch'

def test_handling_of_server_message_parsers():
    for parser_type in PARSER_TYPES:
        run_parser_handling_of_server_message_test(parser_type)
