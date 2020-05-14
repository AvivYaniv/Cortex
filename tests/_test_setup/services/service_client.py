
import pytest

from cortex.client.client_service import ClientService
from cortex.client.client_service import DEFAULT_PORT

from tests.test_constants import SERVER_TEST_HOST

@pytest.fixture
def client_service():
    client_service = ClientService(SERVER_TEST_HOST, DEFAULT_PORT)    
    return client_service
