
import time

import functools

from multiprocessing import Value

import pytest

from tests.integration.tools.main_create_example_mind import EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION

from cortex.client.client_service import ClientService
# from cortex.client.client_service import 

from cortex.utils import delete_under_folder

from cortex.server import run_server
from cortex.server.server_handler import ServerHandler
    
from tests.test_constants import *

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 1234
    
def delete_server_user_folder_before_and_after(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        user_id=TEST_USER_ID
        user_snapshots_path = ServerHandler.get_user_snapshots_path(user_id)
        delete_under_folder(user_snapshots_path)
        result = function(*args, **kwargs)
        delete_under_folder(user_snapshots_path)
        return result
    return wrapper
    
@pytest.fixture
def client_service():
    client_service = ClientService(DEFAULT_HOST, DEFAULT_PORT)    
    return client_service

@delete_server_user_folder_before_and_after
def test_client_service(client_service, capsys):
    test_server_snapshot_published_counter = Value('i', 0)    
    def run_server_thread(test_server_snapshot_published_counter):
        def snapshot_publish(message):            
            test_server_snapshot_published_counter.value += 1            
        run_server(DEFAULT_HOST, DEFAULT_PORT, publish=snapshot_publish)
    import multiprocessing
    server_thread = multiprocessing.Process(target=run_server_thread, args=(test_server_snapshot_published_counter, None))
    server_thread.start()
    client_service.upload_sample(EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION)
    time.sleep(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_service.total_snapshots_uploaded)    
    server_thread.kill()    
    assert client_service.total_snapshots_uploaded == test_server_snapshot_published_counter.value
