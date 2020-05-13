
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.parsers import run_parser_service

if "__main__" == __name__:
    parser_type = 'user_feelings'
    parser_service = run_parser_service(parser_type)
    parser_service.run()
    
