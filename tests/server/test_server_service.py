
import time

import multiprocessing
from multiprocessing import Value
from multiprocessing import Manager

import pytest

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from cortex.server import run_server

from tests._utils.list import is_interleaved_list

from cortex.server.server_handler import ServerHandler

from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

from cortex.utils.folder import count_folders_subfolders

from tests.test_constants import get_test_user
from tests.test_constants import SERVER_TEST_HOST, SERVER_SNAPSHOT_MAX_DURATION_HANDLING

from tests._test_setup.services import run_client_service
from tests._test_setup import delete_server_user_folder_before_and_after

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

@delete_server_user_folder_before_and_after(get_test_user(1).ID)
@delete_server_user_folder_before_and_after(get_test_user(2).ID)
def test_server_service_multiple_clients():
    # Creating shared-memory value to count published snapshots
    test_server_snapshot_published_counter  = Value('i', 0)    
    test_server_snapshot_published_ids      = Manager().list()
    def run_server_service(test_server_snapshot_published_counter, test_server_snapshot_published_ids):
        def snapshot_publish(message):
            snapshot    = MessageQueueMessages().get_message(MessageQueueMessagesTyeps.RAW_SNAPSHOT_MESSAGE).deserialize(message)
            user_id     = snapshot.user_info.user_id 
            test_server_snapshot_published_ids.append(user_id)
            # Update shared-memory published snapshots counter
            test_server_snapshot_published_counter.value += 1            
        run_server(SERVER_TEST_HOST, DEFAULT_PORT, publish=snapshot_publish)
    # Spawn process for server thread
    server_proccess = multiprocessing.Process(target=run_server_service, args=[test_server_snapshot_published_counter, test_server_snapshot_published_ids])
    server_proccess.start()    
    # Clients processes handling
    test_users_ids                      = [ get_test_user(1).ID, get_test_user(2).ID ]
    test_users_snapshots_counters       = [ ]
    client_proccesses_list              = [ ]     
    # Create process for client threads
    for user_proccess_index in range(len(test_users_ids)):
        user_id                         = int(test_users_ids[user_proccess_index])
        client_sent_snapshots_counter   = Value('i', 0)
        test_users_snapshots_counters.append(client_sent_snapshots_counter)
        client_proccess = multiprocessing.Process(target=run_client_service, args=[client_sent_snapshots_counter, user_id])
        client_proccesses_list.append(client_proccess)
    # Spawn client processes
    for client_proccess in client_proccesses_list:    
        client_proccess.start()
        # Tiny sleep to avoid connection reset (which is a matter of security)
        # "It seems like the server side limits the amount of requests per timeunit (hour, day, second) as a security issue." @FelixMartinez
        # https://stackoverflow.com/questions/20568216/python-handling-socket-error-errno-104-connection-reset-by-peer
        time.sleep(0.5)
    # Kill client processes upon finishing
    for client_proccess in client_proccesses_list:
        client_proccess.join()        
        client_proccess.kill()               
    # Wait for server to handle messages and kill it
    total_snapshots_clients_sent = sum([client_sent_snapshots_counter.value for client_sent_snapshots_counter in test_users_snapshots_counters])
    server_proccess.join(SERVER_SNAPSHOT_MAX_DURATION_HANDLING * total_snapshots_clients_sent)
    server_proccess.kill()    
    # Ensuring requests order is interleaved
    assert is_interleaved_list(test_server_snapshot_published_ids)    
    # Ensure snapshots have been published
    assert 0 < test_server_snapshot_published_counter.value
    assert total_snapshots_clients_sent == test_server_snapshot_published_counter.value
    # Ensure total snapshots folders is as much as snapshots in file
    for user_proccess_index in range(len(test_users_ids)): 
        user_id                         = test_users_ids[user_proccess_index]
        total_snapshots_folders = count_folders_subfolders(ServerHandler.get_user_snapshots_path(user_id))
        assert total_snapshots_folders == test_users_snapshots_counters[user_proccess_index].value
    
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
    total_snapshots_folders = count_folders_subfolders(ServerHandler.get_user_snapshots_path(get_test_user(1).ID))
    assert total_snapshots_folders == client_sent_snapshots_counter.value  
    