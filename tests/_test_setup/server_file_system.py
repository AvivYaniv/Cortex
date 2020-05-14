
import functools 

from tests.test_constants import TEST_USER_1_ID

from cortex.utils import delete_under_folder
from cortex.server.server_handler import ServerHandler

def delete_server_user_folder_before_and_after(user_id=TEST_USER_1_ID):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):            
            user_snapshots_path = ServerHandler.get_user_snapshots_path(user_id)
            delete_under_folder(user_snapshots_path)
            result = function(*args, **kwargs)
            delete_under_folder(user_snapshots_path)
            return result
        return wrapper
    return decorator

    