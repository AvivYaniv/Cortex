
import multiprocessing
from multiprocessing import Value

import time

import pytest

from tests.test_constants import DEFAULT_FILE_VERSION

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.server import run_server

from tests.test_constants import get_test_user
from tests.test_constants import SERVER_TEST_HOST, SERVER_SNAPSHOT_MAX_DURATION_HANDLING

from tests.test_constants import get_user_test_file_path

from tests._test_setup import delete_server_user_folder_before_and_after
from tests._test_setup.services import client_service, run_client_service

def test_client_file_not_found(client_service, capsys):
    NON_EXISTANT_FILE_NAME = 'non_existant_file'
    client_service.upload_sample(NON_EXISTANT_FILE_NAME, DEFAULT_FILE_VERSION)
    out, _ = capsys.readouterr()
    assert ClientService.get_file_not_found_message(NON_EXISTANT_FILE_NAME) in out

@delete_server_user_folder_before_and_after()
def test_client_service(client_service):
    # Creating shared-memory value to count published snapshots
    test_server_snapshot_published_counter = Value('i', 0)    
    def run_server_service(test_server_snapshot_published_counter):
        def snapshot_publish(message):
            # Update shared-memory published snapshots counter
            test_server_snapshot_published_counter.value += 1            
        run_server(SERVER_TEST_HOST, DEFAULT_PORT, publish=snapshot_publish)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_service, args=[test_server_snapshot_published_counter])
    server_proccess.start()
    # Upload to server
    client_service.upload_sample(get_user_test_file_path(get_test_user(1).ID), DEFAULT_FILE_VERSION)
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_service._total_snapshots_uploaded)
    server_proccess.kill()
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert client_service._total_snapshots_uploaded == test_server_snapshot_published_counter.value

@delete_server_user_folder_before_and_after()
def test_client_service_as_server_startup_delayed(client_service):
    # Creating shared-memory value to count sent snapshots
    client_sent_snapshots_counter = Value('i', 0)
    # Spawn process for client thread and kill it upon finishing
    client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter])
    client_proccess.start()
    # Sleep to simulate server delay at startup
    time.sleep(10)
    # Creating shared-memory value to count published snapshots
    test_server_snapshot_published_counter = Value('i', 0)    
    def run_server_service(test_server_snapshot_published_counter):
        def snapshot_publish(message):
            # Update shared-memory published snapshots counter
            test_server_snapshot_published_counter.value += 1            
        run_server(SERVER_TEST_HOST, DEFAULT_PORT, publish=snapshot_publish)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_service, args=[test_server_snapshot_published_counter])
    server_proccess.start()    
    # Spawn process for client thread and kill it upon finishing
    client_proccess.join()
    client_proccess.kill()    
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_sent_snapshots_counter.value)
    server_proccess.kill()    
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert client_sent_snapshots_counter.value == test_server_snapshot_published_counter.value
