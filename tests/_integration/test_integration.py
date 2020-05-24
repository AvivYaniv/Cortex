
import sys

import time

import requests

import multiprocessing
from multiprocessing import Value
from multiprocessing import Manager

import pytest

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.server.server_service import run_server_service

from cortex.server.server_handler import ServerHandler

from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

from cortex.utils.folder import count_folders_subfolders

from tests.test_constants import get_test_user
from tests.test_constants import API_TEST_HOST, SERVER_TEST_HOST, MESSAGE_QUEUE_TEST_HOST, DB_TEST_HOST
from tests.test_constants import SERVER_SNAPSHOT_MAX_DURATION_HANDLING

from tests._test_setup.services import run_client_service
from tests._test_setup import delete_server_user_folder_before_and_after

from tests.test_constants import PARSER_TYPES
from tests.test_constants import get_message_queue_mesages_file_path
from cortex.utils.files.file_handler import _FileHandler

from cortex.server.server_service import ServerService
from cortex.parsers.parser_service import ParserService
from cortex.saver.saver_service import SaverService

from tests.test_constants import get_api_results_file_path

from tests.test_constants import is_on_ci_environment

from tests.test_constants import PARSER_TYPES
from tests.test_constants import DEFAULT_END_TO_END_DURATION
from tests.test_constants import DEFAULT_INITIALIZATION_DURATION
from cortex.parsers import run_parser_service

from cortex.saver import run_saver_service

from cortex.api.api_urls import get_custom_api_url
from cortex.api.api_urls import API_URL_FORMAT_GET_ALL_USER_RESULTS
from cortex.api.api_urls import DEFAULT_API_HOSTNAME

from cortex.api.api_server import run_api

from cortex.api.api_urls import DEFAULT_API_PORT

from cortex.utils import change_direcoty_to_project_root

from cortex.database.database_runner import run_database

from cortex.publisher_consumer.message_queue.message_queue_runner import install_message_queue

def run_proceess(run_function):
    proccess = multiprocessing.Process(target=run_function)
    proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    return proccess

def run_database_proceess():
    return run_proceess(run_database)

def run_messagequeue_proceess():
    return run_proceess(install_message_queue)

def run_api_proceess():
    def run_api_test_host():
        run_api(host=API_TEST_HOST, database_host=DB_TEST_HOST)
    api_proccess = multiprocessing.Process(target=run_api_test_host)
    api_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    return api_proccess
    
def run_parser_proceess(parser_type):
    parser_proccess = multiprocessing.Process(target=run_parser_service, args=[parser_type, None, MESSAGE_QUEUE_TEST_HOST])
    parser_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    return parser_proccess
    
def run_saver_proceess():
    def run_saver_test_host():
        run_saver_service(database_host=DB_TEST_HOST, message_queue_host=MESSAGE_QUEUE_TEST_HOST)
    saver_proccess = multiprocessing.Process(target=run_saver_test_host)
    saver_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    return saver_proccess

def assert_integration_success(user_id):
    user_id                     = str(user_id)
    api_results_file_path       = get_api_results_file_path(user_id)
    user_api_results_expected   = _FileHandler.read_file(api_results_file_path)
    api_url                     = get_custom_api_url(API_URL_FORMAT_GET_ALL_USER_RESULTS, { '%user_id%' : user_id }, host=f'http://{API_TEST_HOST}:{DEFAULT_API_PORT}')
    user_api_results_actual     = requests.get(api_url).text
    assert user_api_results_expected == user_api_results_actual
    
@delete_server_user_folder_before_and_after()
@change_direcoty_to_project_root()
def test_integration():
    micro_services_proceess = []
    # If not on CI - Travis already configured to have database and message-queue
    if not is_on_ci_environment():
        # Running MessageQueue
        micro_services_proceess.append(run_messagequeue_proceess())    
        # Running DataBase
        micro_services_proceess.append(run_database_proceess())
    # Running saver process
    micro_services_proceess.append(run_saver_proceess())
    # Running parsers
    for parser_type in PARSER_TYPES:
        micro_services_proceess.append(run_parser_proceess(parser_type))
    # Creating shared-memory value to count sent snapshots
    client_sent_snapshots_counter   = Value('i', 0)
    # Creating shared-memory value to get sent user id
    client_sent_user_id             = Value('i', 0)
    def run_server_process():
        run_server_service(host=SERVER_TEST_HOST, port=DEFAULT_PORT, message_queue_host=MESSAGE_QUEUE_TEST_HOST)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_process)
    server_proccess.start()    
    # Spawn process for client thread and kill it upon finishing
    client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter, None, client_sent_user_id])
    client_proccess.start()
    client_proccess.join()
    client_proccess.kill()    
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_sent_snapshots_counter.value)
    server_proccess.kill()
    # Running API server
    micro_services_proceess.append(run_api_proceess())
    # Waiting for snapshots to pass end to end
    time.sleep(DEFAULT_END_TO_END_DURATION * client_sent_snapshots_counter.value)
    # Asserting integration success
    assert_integration_success(client_sent_user_id.value)
    # Killing remaining micro-services processes
    for micro_service_proceess in micro_services_proceess:
        micro_service_proceess.kill()
        