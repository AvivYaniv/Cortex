
from cortex.utils import create_files_folder_path

from cortex.utils import generate_uuid

from cortex.utils import change_direcoty_to_project_root

from cortex.utils import _FileHandler

from tests.test_constants import get_message_queue_mesages_file_path 

@change_direcoty_to_project_root()
def write_message(message,                  \
                  sender_service_name,      \
                  reciver_service_name,     \
                  sender_identifier=None,   \
                  reciver_identifier=None,  \
                  rewrite=None):
    if not message:
        return
    rewrite             = rewrite if rewrite else True
    rewrite_prefix      = '' if rewrite else generate_uuid()
    message             = message if isinstance(message, str) else message.decode('utf-8')     
    message_file_path   = get_message_queue_mesages_file_path(  \
                            sender_service_name,                \
                            reciver_service_name,               \
                            sender_identifier,                  \
                            reciver_identifier,                 \
                            rewrite_prefix)
    create_files_folder_path(message_file_path)
    _file_handler = _FileHandler()
    _file_handler.save(message_file_path, message)
    
def write_messages_class_method_decorator(func,             \
                                          incoming_end,     \
                                          service_name,     \
                                          outgoing_end,     \
                                          identifier=None,  \
                                          rewrite=None):
    """
        <incoming_end> => <[identifier] + service_name> => outgoing_end
    """    
    def inner(self, incoming_message): 
        write_message(incoming_message,                     \
                      incoming_end,                         \
                      service_name,                         \
                      reciver_identifier=identifier,        \
                      rewrite=rewrite)
        output_message_object = func(self, incoming_message)
        write_message(output_message_object.serialize(),    \
                      service_name,                         \
                      outgoing_end,                         \
                      sender_identifier=identifier,         \
                      rewrite=rewrite)
        return output_message_object 
    return inner
