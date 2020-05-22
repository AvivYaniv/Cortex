
from cortex.parsers import run_parser_service

from cortex.utils import change_direcoty_to_project_root

@change_direcoty_to_project_root()
def run_parser_service_at_root_directory(parser_type):
    parser_service = run_parser_service(parser_type)
    parser_service.run() 

if "__main__" == __name__:
    parser_type = 'pose'
    run_parser_service_at_root_directory(parser_type)
    