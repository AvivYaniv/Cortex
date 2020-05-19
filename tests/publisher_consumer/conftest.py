
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time

import pytest

import multiprocessing

from tests.test_constants import PARSER_TYPES
from tests.test_constants import SAVER_MOCK_DEFAULT_IDS

from cortex.publisher_consumer.message_queue.message_queue_runner import install_message_queue
from cortex.publisher_consumer.message_queue.message_queue_runner import shutdown_message_queue

from cortex.utils import delete_under_folder

from tests._utils import start_proccesses
from tests._utils import stop_proccesses

from tests.publisher_consumer.main_mq_saver_mock import run_saver_mock
from tests.publisher_consumer.main_mq_parser_mock import run_parser_mock
from tests.publisher_consumer.main_mq_server_mock import run_server_mock

from tests.test_constants import CI_CD_TEST_ENVIRONMENT

from tests.test_constants import SERVER_MESSAGES_IDS

from tests.test_constants import MESSAGE_QUEUE_TYPE
from tests.test_constants import DEFAULT_JOIN_DURATION, DEFAULT_INITIALIZATION_DURATION, DEFAULT_PROCCESS_DURATION

from tests.test_constants import get_message_queue_serivce_outputs_path

def pytest_sessionstart(session):
    delete_under_folder(get_message_queue_serivce_outputs_path())
    assert install_message_queue(MESSAGE_QUEUE_TYPE)
    run_services_according_to_mesage_queue_configuration()

def pytest_sessionfinish(session, exitstatus):
    if CI_CD_TEST_ENVIRONMENT not in os.environ:
        shutdown_message_queue(MESSAGE_QUEUE_TYPE)
        delete_under_folder(get_message_queue_serivce_outputs_path())
    
def run_services_according_to_mesage_queue_configuration():
    # Start savers services
    saver_proccesses    = start_proccesses(run_saver_mock, SAVER_MOCK_DEFAULT_IDS)
    # Start parsers services
    parser_proccesses   = start_proccesses(run_parser_mock, PARSER_TYPES)
    # Allow services to initialize
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    # Start server
    server_proccess = multiprocessing.Process(target=run_server_mock)
    server_proccess.start()  
    server_proccess.join(DEFAULT_JOIN_DURATION)
    server_proccess.kill()
    # Wait duration for processing
    processing_wait_duration = DEFAULT_PROCCESS_DURATION * len(SERVER_MESSAGES_IDS)
    # Stop parsers services
    stop_proccesses(parser_proccesses, processing_wait_duration)
    # Stop savers services
    stop_proccesses(saver_proccesses, processing_wait_duration)
        