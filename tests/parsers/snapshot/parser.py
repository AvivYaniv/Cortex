
from cortex.parsers.snapshot.parser_handler import ParserHandler

from tests.test_constants import get_raw_snapshot_file_path
from tests.test_constants import get_raw_snapshot_result_path

from cortex.parsers.snapshot.parser_file_handler import ParserFileHandler

def parse(parser_type, raw_snapshot_path):
    """
    Accepts a parser name and a path to some raw data, 
    and prints the result, as published to the message queue 
    (optionally redirecting it to a file).
    """
    parser          = ParserHandler(parser_type)
    result, _       = parser.parse_raw_snapshot_file(raw_snapshot_path)
    return result

def parse_test_raw_snapshot(parser_type):
    raw_snapshot_file_path = get_raw_snapshot_file_path()
    return parse(parser_type, raw_snapshot_file_path)

def _save_snapshot_result(parser_type, is_binary_result_file):
    mode = 'wb' if is_binary_result_file else 'w'
    result = parse_test_raw_snapshot(parser_type)
    parser_file_handler = ParserFileHandler()
    parser_file_handler.save_file(get_raw_snapshot_result_path(parser_type), result, mode)
    
def run_snapshot_parser_test(parser_type, is_binary_result_file):
    mode = 'rb' if is_binary_result_file else 'r'
    snapshot_result_file_path       = get_raw_snapshot_result_path(parser_type)
    with open(snapshot_result_file_path, mode) as f:
        snapshot_expected_result    = f.read()
    snapshot_actual_result          = parse_test_raw_snapshot(parser_type)
    assert snapshot_actual_result == snapshot_expected_result
        