
from cortex.server import run_server

from cortex.utils import change_direcoty_to_project_root

@change_direcoty_to_project_root()
def run_server_at_root_directory(host, port):
    run_server(host, port)
    
if "__main__" == __name__:
    host, port = '127.0.0.1', '8000'    
    run_server_at_root_directory(host, port)
    