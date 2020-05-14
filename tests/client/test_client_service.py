
import time

import functools

import multiprocessing
from multiprocessing import Value

import pytest

from tests._tools.main_create_example_mind import EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.utils import delete_under_folder

from cortex.server import run_server
from cortex.server.server_handler import ServerHandler
    
from tests.test_constants import *
   
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
    client_service = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)    
    return client_service

@delete_server_user_folder_before_and_after
def test_client_service(client_service):
    # Creating shared-memory value to count published snapshots
    test_server_snapshot_published_counter = Value('i', 0)    
    def run_server_thread(test_server_snapshot_published_counter):
        def snapshot_publish(message):
            # Update shared-memory published snapshots counter
            test_server_snapshot_published_counter.value += 1            
        run_server(SERVER_TEST_HOST, DEFAULT_PORT, publish=snapshot_publish)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_thread, args=[test_server_snapshot_published_counter])
    server_proccess.start()
    # Upload to server
    client_service.upload_sample(EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION)
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_service.total_snapshots_uploaded)
    server_proccess.kill()
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert client_service.total_snapshots_uploaded == test_server_snapshot_published_counter.value
