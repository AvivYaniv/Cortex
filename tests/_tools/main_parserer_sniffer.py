
from cortex.server import run_server

import cortex.server.server_handler

from cortex.server.server_handler import ServerHandler

import cortex.utils.consts

from tests.test_constants import get_raw_snapshot_folder_path, get_raw_snapshot_folder_relative_path

from cortex.utils import delete_under_folder

from tests._utils.message_writer import write_messages_class_method_decorator

import multiprocessing

import cortex.parsers.parser_service as parser_service

from tests.test_constants import PARSER_TYPES
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
def run_patched_parser_at_root_directory(parser_type):
    patch_parser_handler(parser_type)
    run_parser_service(parser_type)
    
def run_parser_proceess(parser_type):
    parser_proccess = multiprocessing.Process(target=run_patched_parser_at_root_directory, args=[parser_type])
    parser_proccess.start()

def run_patched_server():
    @change_direcoty_to_project_root()
    def run_server_at_root_directory(host, port):
        delete_under_folder(get_raw_snapshot_folder_path())
        run_server(host, port)
    def _get_snapshot_save_path(self, snapshot_uuid):
        return cortex.server.server_handler.ServerHandler._get_save_path(  \
                    get_raw_snapshot_folder_relative_path(),               \
                    cortex.server.server_handler.SNAPSHOT_FILE_NAME)         
    def patch_server_save_file_path():    
        cortex.server.server_handler.ServerHandler._get_snapshot_save_path = \
            _get_snapshot_save_path  
    host, port = '127.0.0.1', '8000'
    patch_server_save_file_path()
    run_server_at_root_directory(host, port)

def run_server_process():
    server_proccess = multiprocessing.Process(target=run_patched_server)
    server_proccess.start()

if "__main__" == __name__:
    run_server_process()
    for parser_type in PARSER_TYPES:
        run_parser_proceess(parser_type)
        