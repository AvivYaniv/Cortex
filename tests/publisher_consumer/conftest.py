
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import multiprocessing

from tests.test_constants import PARSER_TYPES
from tests.test_constants import SAVER_MOCK_DEFAULT_IDS

from cortex.publisher_consumer.message_queue.message_queue_runner import install_message_queue
from cortex.publisher_consumer.message_queue.message_queue_runner import shutdown_message_queue

from cortex.utils import delete_under_folder

from tests.publisher_consumer.main_mq_saver_mock import run_saver_mock
from tests.publisher_consumer.main_mq_parser_mock import run_parser_mock
from tests.publisher_consumer.main_mq_server_mock import run_server_mock

from tests.test_constants import SERVER_MESSAGES_IDS

from tests.test_constants import MESSAGE_QUEUE_TYPE
from tests.test_constants import DEFAULT_JOIN_DURATION, DEFAULT_INITIALIZATION_DURATION, DEFAULT_PROCCESS_DURATION

from tests.test_constants import get_message_queue_messages_path

def pytest_sessionstart(session):
    delete_under_folder(get_message_queue_messages_path())
    assert install_message_queue(MESSAGE_QUEUE_TYPE)
    run_services_according_to_mesage_queue_configuration()

def pytest_sessionfinish(session, exitstatus):
    shutdown_message_queue(MESSAGE_QUEUE_TYPE)
    delete_under_folder(get_message_queue_messages_path())
    
def _start_proccesses(run_function, service_ids_list):
    proccesses = []
    for service_id in service_ids_list:   
        proccess = multiprocessing.Process(target=run_function, args=[ service_id ])
        proccess.start()  
        proccesses.append(proccess)
    return proccesses

def _stop_proccesses(proccesses, processing_wait_duration):
    time.sleep(processing_wait_duration)
    for proccess in proccesses:
        proccess.join(DEFAULT_JOIN_DURATION)
        proccess.kill()

def run_services_according_to_mesage_queue_configuration():
    # Start savers services
    saver_proccesses    = _start_proccesses(run_saver_mock, SAVER_MOCK_DEFAULT_IDS)
    # Start parsers services
    parser_proccesses   = _start_proccesses(run_parser_mock, PARSER_TYPES)
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
    _stop_proccesses(parser_proccesses, processing_wait_duration)
    # Stop savers services
    _stop_proccesses(saver_proccesses, processing_wait_duration)
        