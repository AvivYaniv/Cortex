
import pytest

from tests.parsers.snapshot.parser import run_snapshot_parser_test

# NOTE: Change to True if result file is binary
IS_BINARY_RESULT_FILE   =   True

PARSER_TYPE             =   'depth_image'

def _create_template_result():
    from tests.parsers.snapshot.parser import _save_snapshot_result
    _save_snapshot_result(PARSER_TYPE, IS_BINARY_RESULT_FILE)
    
def test_template_parser():
    _create_template_result()
    """
    # NOTE: Remove after first run <start>
    _create_template_result(SAVE_RESULT_FILE_MODE)
    # NOTE: Remove after first run <end>
    run_snapshot_parser_test(PARSER_TYPE, IS_BINARY_RESULT_FILE)
    """
    assert 'Uncomment to create new parser test' == 'Uncomment to create new parser test'
    