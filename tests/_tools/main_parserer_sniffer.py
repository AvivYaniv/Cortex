
from tests._utils.message_writer import write_messages_class_method_decorator

import cortex.parsers.parser_service as parser_service

from cortex.parsers import run_parser_service

from cortex.utils import change_direcoty_to_project_root

from cortex.server.server_service import ServerService
from cortex.parsers.parser_service import ParserService
from cortex.saver.saver_service import SaverService 

def patch_parser_handler(parser_type):
    parser_service.ParserService.parse_message =        \
        write_messages_class_method_decorator(          \
            parser_service.ParserService.parse_message, \
            ServerService.SERVICE_TYPE,                 \
            ParserService.SERVICE_TYPE,                 \
            SaverService.SERVICE_TYPE,                  \
            parser_type)
    
@change_direcoty_to_project_root()
def run_parser_at_root_directory(parser_type):
    run_parser_service(parser_type)
    
if "__main__" == __name__:
    parser_type = 'depth_image'
    patch_parser_handler(parser_type)
    run_parser_at_root_directory(parser_type)
    