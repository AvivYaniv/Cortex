
import pytest

from tests.parsers.snapshot.parser import run_snapshot_parser_test

IS_BINARY_RESULT_FILE   =   False
PARSER_TYPE             =   'pose'

def test_pose_parser():
    run_snapshot_parser_test(PARSER_TYPE, IS_BINARY_RESULT_FILE)
