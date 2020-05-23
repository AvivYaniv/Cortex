
from cortex.api.api_server import run_api

from cortex.utils import change_direcoty_to_project_root

@change_direcoty_to_project_root()
def run_api_server_at_root():
    run_api()

if "__main__" == __name__:
    run_api_server_at_root()
