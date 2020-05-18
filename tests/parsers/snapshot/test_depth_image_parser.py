
import pytest

from tests.parsers.snapshot.parser import run_snapshot_parser_test

IS_BINARY_RESULT_FILE   =   True
PARSER_TYPE             =   'depth_image'

def test_depth_image_parser():    
    run_snapshot_parser_test(PARSER_TYPE, IS_BINARY_RESULT_FILE)
    