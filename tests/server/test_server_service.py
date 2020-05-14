
import multiprocessing
from multiprocessing import Value

import pytest

from tests._tools.main_create_example_mind import EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.server import run_server

from tests.test_constants import SERVER_TEST_HOST, SERVER_SNAPSHOT_MAX_DURATION_HANDLING

from tests._test_setup import delete_server_user_folder_before_and_after
from flask.cli import cli

@delete_server_user_folder_before_and_after
def test_server_service():
    client_sent_snapshots_counter = Value('i', 0)
    def run_client_service(client_sent_snapshots_counter):        
        client_service = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)
        # Upload to server
        client_service.upload_sample(EXAMPLE_FILE_PATH, DEFAULT_FILE_VERSION)
        client_sent_snapshots_counter.value = client_service.total_snapshots_uploaded         
    
    test_server_snapshot_published_counter = Value('i', 0)    
    def run_server_service(test_server_snapshot_published_counter):
        def snapshot_publish(message):
            # Update shared-memory published snapshots counter
            test_server_snapshot_published_counter.value += 1            
        run_server(SERVER_TEST_HOST, DEFAULT_PORT, publish=snapshot_publish)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_service, args=[test_server_snapshot_published_counter])
    server_proccess.start()
    
    # Spawn process for server thread
    client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter])
    client_proccess.start()
    client_proccess.join()
    client_proccess.kill()
    
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_sent_snapshots_counter.value)
    server_proccess.kill()
    
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert client_sent_snapshots_counter.value == test_server_snapshot_published_counter.value
