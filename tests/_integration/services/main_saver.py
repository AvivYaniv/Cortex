
from cortex.saver import run_saver_service

from cortex.utils import change_direcoty_to_project_root

@change_direcoty_to_project_root()
def run_saver_service_at_root_directory():
    run_saver_service()   
    
if "__main__" == __name__:
    run_saver_service_at_root_directory()   
