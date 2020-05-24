
import pytest

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from tests.test_constants import get_test_user
from tests.test_constants import DEFAULT_FILE_VERSION
from tests.test_constants import get_user_test_file_path
from tests.test_constants import SERVER_TEST_HOST

@pytest.fixture
def client_service():
    client_service = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)    
    return client_service

def run_client_service(client_sent_snapshots_counter, test_user_id=None, client_sent_user_id=None):        
    client_service  = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)
    test_user_id    = test_user_id if test_user_id else get_test_user(1).ID
    test_file_path  = get_user_test_file_path(test_user_id)
    # Upload to server
    client_service.upload_sample(test_file_path, DEFAULT_FILE_VERSION)
    client_sent_snapshots_counter.value = client_service._total_snapshots_uploaded
    if client_sent_user_id:
        client_sent_user_id.value       = client_service._user_id
    