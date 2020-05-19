
import pytest

from tests.test_constants import PARSER_SERVICE_TYPE

from tests.test_constants import get_saver_message_queue_mesages_file_path

def test_saver_parsers_messages():
    for parser_type in PARSER_SERVICE_TYPE:
        parser_message_file_path = get_saver_message_queue_mesages_file_path(parser_type)
        
    assert False
    