
import pytest

from tests.parsers.snapshot.parser import run_snapshot_parser_test

IS_BINARY_RESULT_FILE   =   False
PARSER_TYPE             =   'user_feelings'

def test_user_feelings_parser():
    run_snapshot_parser_test(PARSER_TYPE, IS_BINARY_RESULT_FILE)
    