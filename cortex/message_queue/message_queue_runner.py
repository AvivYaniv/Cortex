import os 
from cortex.utils import DynamicModuleLoader 
from cortex.utils import run_bash_scipt
from cortex.utils import get_project_file_path_by_caller

from cortex.message_queue.rabbitmq_mq import RabbitMQMessageQueue

import logging
from cortex.logger import LoggerLoader
from cortex.message_queue.rabbitmq_mq import RabbitMQMessageQueue

# Log loading
logger_loader             = LoggerLoader()
logger_loader.load_log_config()
logger                    = logging.getLogger(__name__)

# Messages Section
# Info Messages
INSTALLING_MESSAGE_QUEUE_INFO_MESSAGE                           =   'Installing message queue...'

# Error messages
MESSAGE_QUEUE_TYPE_NOT_FOUND_ERROR_MESSAGE                      =   'Specified message queue class not found in directory'
MESSAGE_QUEUE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT    =   'Message queue install file {} dosen\'t exist'
MESSAGE_QUEUE_INSTALLATION_FAILED_ERROR_MESSAGE                 =   'Message queue installation has failed'

# Installation file
MESSAGE_QUEUE_INSTALLATION_FILE_SUFFIX              			=   '_install.sh'

def load_message_queue(callback, message_queue_context, message_queue_type, host):
    LOOKUP_TOKEN        =   'MessageQueue'
    NAME_IDENTIFIER     =   'name'
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
    _, class_mqs = \
        DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, LOOKUP_TOKEN, NAME_IDENTIFIER)
    if message_queue_type not in class_mqs:
        logger.error(MESSAGE_QUEUE_TYPE_NOT_FOUND_ERROR_MESSAGE)
        return None
    # Returning specified message queue object
    return class_mqs[message_queue_type](logger, callback, message_queue_context, host)

def get_message_install_file_path(message_queue_type):
    return get_project_file_path_by_caller(message_queue_type, MESSAGE_QUEUE_INSTALLATION_FILE_SUFFIX)

def install_message_queue(message_queue_type):
    # Installing message queue
    message_queue_install_file_path = get_message_install_file_path(message_queue_type)
    
    # If message queue install file dosen't exist
    if (not os.path.isfile(message_queue_install_file_path)):
        logger.error(MESSAGE_QUEUE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(message_queue_install_file_path))
        return False
    
    # Installing message queue
    logger.info(INSTALLING_MESSAGE_QUEUE_INFO_MESSAGE)
    intallation_success = (0 == run_bash_scipt(message_queue_install_file_path)) 
    if not intallation_success:
        logger.error(MESSAGE_QUEUE_INSTALLATION_FAILED_ERROR_MESSAGE)
    return intallation_success

def run_message_queue(message_queue_context,
					  callback				 =	 None, 
					  message_queue_type     =   RabbitMQMessageQueue.name,
					  host                   =   'localhost'):
    message_queue = load_message_queue(callback, message_queue_context, message_queue_type, host)
    # If message queue not found - exit
    if not message_queue:
        return
    # Else, message queue found - install & run
    else:
        # If message queue installed
        if install_message_queue(message_queue_type):
            return message_queue.run()
    