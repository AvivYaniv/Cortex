
import pytest

from cortex.saver.saver import Saver

from cortex.saver.saver_service import SaverService 

from cortex.parsers.parser_service import ParserService

from tests.test_constants import get_message_queue_mesages_file_path

@pytest.fixture
def saver_service():
    saver       = Saver()
    _database   = saver.get_database()
    _database.driver._clear()
    return saver

def run_saver_handling_of_parser_message_test(saver_service, parser_type):
    parser_message_file_path                = get_message_queue_mesages_file_path(  \
                                                ParserService.SERVICE_TYPE,         \
                                                SaverService.SERVICE_TYPE,          \
                                                sender_identifier=parser_type)
    snapshot_uuid                           = saver_service.save(parser_message_file_path)
    _database                               = saver_service.get_database()
    database_save_validation_function_name  = f'get_{parser_type}'
    assert getattr(_database, database_save_validation_function_name)(snapshot_uuid=snapshot_uuid) is not None, f'Saver failed to save {parser_type}'

def test_saver_parser_message_user_feelings(saver_service):
    run_saver_handling_of_parser_message_test(saver_service, 'user_feelings')

def test_saver_parser_message_pose(saver_service):
    run_saver_handling_of_parser_message_test(saver_service, 'pose')

def test_saver_parser_message_color_image(saver_service):
    run_saver_handling_of_parser_message_test(saver_service, 'color_image')
    
def test_saver_parser_message_depth_image(saver_service):
    run_saver_handling_of_parser_message_test(saver_service, 'depth_image')
    