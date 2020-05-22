
from cortex.server import run_server

import cortex.server.server_handler

from cortex.server.server_handler import ServerHandler

import cortex.utils.consts

from tests.test_constants import get_raw_snapshot_folder_path

from cortex.utils import change_direcoty_to_project_root

from cortex.utils import delete_under_folder

@change_direcoty_to_project_root()
def run_server_at_root_directory(host, port):
    delete_under_folder(get_raw_snapshot_folder_path())
    run_server(host, port)

def _get_snapshot_save_path(self, snapshot_uuid):
    return cortex.server.server_handler.ServerHandler._get_save_path(  \
                get_raw_snapshot_folder_path(),                        \
                cortex.server.server_handler.SNAPSHOT_FILE_NAME) 
    
def patch_server_save_file_path():    
    cortex.server.server_handler.ServerHandler._get_snapshot_save_path = \
        _get_snapshot_save_path
    
if "__main__" == __name__:
    host, port = '127.0.0.1', '8000'
    patch_server_save_file_path()
    run_server_at_root_directory(host, port)
    