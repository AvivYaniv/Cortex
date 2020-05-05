
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.parsers import run_parser_service

if "__main__" == __name__:
    parser_type     = 'depth_image'
    parser_service  = run_parser_service(parser_type)
    parser_service.run()
    