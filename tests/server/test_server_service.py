
import time

import multiprocessing
from multiprocessing import Value

import pytest

from tests._tools.main_create_example_mind import DEFAULT_FILE_VERSION

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.server import run_server

from cortex.server.server_handler import ServerHandler

from cortex.utils.folder import count_folders_subfolders

from tests.test_constants import TEST_USER_1_ID, TEST_USER_2_ID
from tests.test_constants import SERVER_TEST_HOST, SERVER_SNAPSHOT_MAX_DURATION_HANDLING

from tests.test_constants import get_user_test_file_path

from tests._test_setup import delete_server_user_folder_before_and_after

def run_client_service(client_sent_snapshots_counter, test_user_id=None):        
    client_service  = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)
    test_user_id    = test_user_id if test_user_id else TEST_USER_1_ID
    test_file_path  = get_user_test_file_path(test_user_id)
    # Upload to server
    client_service.upload_sample(test_file_path, DEFAULT_FILE_VERSION)
    client_sent_snapshots_counter.value = client_service.total_snapshots_uploaded  

@delete_server_user_folder_before_and_after()
def test_server_service():
    # Creating shared-memory value to count sent snapshots
    client_sent_snapshots_counter = Value('i', 0)
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

@delete_server_user_folder_before_and_after(TEST_USER_1_ID)
@delete_server_user_folder_before_and_after(TEST_USER_2_ID)
def test_server_service_multiple_clients():
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
    # Clients processes handling
    test_users_ids                      = [ TEST_USER_1_ID, TEST_USER_2_ID ]
    test_users_snapshots_counters       = [ ]
    client_proccesses_list              = [ ]     
    # Create process for client threads
    for user_proccess_index in range(len(test_users_ids)):
        user_id                         = test_users_ids[user_proccess_index]
        client_sent_snapshots_counter   = Value('i', 0)
        test_users_snapshots_counters.append(client_sent_snapshots_counter)
        client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter, user_id])
        client_proccesses_list.append(client_proccess)
    # Spawn client processes
    for client_proccess in client_proccesses_list:    
        client_proccess.start()
    # Kill client processes upon finishing
    for client_proccess in client_proccesses_list:
        client_proccess.join()        
        client_proccess.kill()               
    # Wait for server to handle messages and kill it
    total_snapshots_clients_sent = sum([client_sent_snapshots_counter.value for client_sent_snapshots_counter in test_users_snapshots_counters])
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * total_snapshots_clients_sent)
    server_proccess.kill()    
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert total_snapshots_clients_sent == test_server_snapshot_published_counter.value
    
@delete_server_user_folder_before_and_after()
def test_server_snapshots_dedup():
    # Creating shared-memory value to count sent snapshots
    client_sent_snapshots_counter = Value('i', 0)
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
    # Uploading twice same file
    for _ in range(2):    
        # Spawn process for client thread and kill it upon finishing
        client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter])
        client_proccess.start()
        client_proccess.join()
        client_proccess.kill()              
    # Wait for server to handle messages and kill it
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * client_sent_snapshots_counter.value)
    server_proccess.kill()        
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    # Ensure number of snapshots published equals the number of snapshots in current last execution, thus, duplicate snapshot uploading won't be published 
    assert client_sent_snapshots_counter.value == test_server_snapshot_published_counter.value
    # Ensure total snapshots folders is as much as snapshots in file
    total_snapshots_folders = count_folders_subfolders(ServerHandler.get_user_snapshots_path(TEST_USER_1_ID))
    assert total_snapshots_folders == client_sent_snapshots_counter.value  
    