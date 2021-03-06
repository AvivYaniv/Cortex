import os 
import threading

from cortex.utils import DynamicModuleLoader 
from cortex.utils import run_bash_scipt
from cortex.utils import get_project_file_path_by_caller

from cortex.publisher_consumer.message_queue.rabbitmq_mq import RabbitMQMessageQueue

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()
logger                    = logging.getLogger(__name__)

# Constants Section
DEFAULT_MESSAGE_QUEUE                                           =   RabbitMQMessageQueue.name

# Locks
installation_lock                                               =   threading.Lock()

# Messages Section
# Info Messages
# Installation info Messages
INSTALLING_MESSAGE_QUEUE_INFO_MESSAGE                           =   'Installing message queue...'
MESSAGE_QUEUE_INSTALLATION_COMPLETED_INFO_MESSAGE               =   'Message queue installation completed!'
# Shutting down info Messages
SHUTTING_DOWN_MESSAGE_QUEUE_INFO_MESSAGE                        =   'Shutting down message queue...'
MESSAGE_QUEUE_SHUT_DOWN_COMPLETED_INFO_MESSAGE                  =   'Message queue shut down completed!'

# Error messages
MESSAGE_QUEUE_TYPE_NOT_FOUND_ERROR_MESSAGE                      =   'Specified message queue class not found in directory'
MESSAGE_QUEUE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT    =   'Message queue install file {} dosen\'t exist'
MESSAGE_QUEUE_SHUTDOWN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT   =   'Message queue shutdown file {} dosen\'t exist'
MESSAGE_QUEUE_INSTALLATION_FAILED_ERROR_MESSAGE                 =   'Message queue installation has failed'
MESSAGE_QUEUE_SHUTDOWN_FAILED_ERROR_MESSAGE                     =   'Message queue shutdown has failed'

# Installation file
MESSAGE_QUEUE_INSTALLATION_FILE_SUFFIX              			=   '_install.sh'

# Shutdown file
MESSAGE_QUEUE_SHUTDOWN_FILE_SUFFIX                              =   '_shutdown.sh'

def load_message_queue(callback, message_queue_context, message_queue_type, host, port):
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
    return class_mqs[message_queue_type](logger, callback, message_queue_context, host, port)

def get_message_install_file_path(message_queue_type):
    return get_project_file_path_by_caller(message_queue_type, MESSAGE_QUEUE_INSTALLATION_FILE_SUFFIX)

def install_message_queue(message_queue_type=None):
    # Default parameter resolution
    message_queue_type = message_queue_type if message_queue_type else DEFAULT_MESSAGE_QUEUE
    # Installing message queue
    message_queue_install_file_path = get_message_install_file_path(message_queue_type)    
    # If message queue install file dosen't exist
    if (not os.path.isfile(message_queue_install_file_path)):
        logger.error(MESSAGE_QUEUE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(message_queue_install_file_path))
        return False    
    # Installing message queue
    logger.info(INSTALLING_MESSAGE_QUEUE_INFO_MESSAGE)
    installation_lock.acquire()
    try:
        intallation_success = (0 == run_bash_scipt(message_queue_install_file_path))
    finally:            
        installation_lock.release()     
    if intallation_success:
        logger.info(MESSAGE_QUEUE_INSTALLATION_COMPLETED_INFO_MESSAGE)
    else:
        logger.error(MESSAGE_QUEUE_INSTALLATION_FAILED_ERROR_MESSAGE)
    return intallation_success

def get_message_shutdown_file_path(message_queue_type):
    return get_project_file_path_by_caller(message_queue_type, MESSAGE_QUEUE_SHUTDOWN_FILE_SUFFIX)

def shutdown_message_queue(message_queue_type=None):
    # Default parameter resolution
    message_queue_type = message_queue_type if message_queue_type else DEFAULT_MESSAGE_QUEUE
    # Shutting down message queue
    message_queue_shutdown_file_path = get_message_shutdown_file_path(message_queue_type)    
    # If message queue shutdown file dosen't exist
    if (not os.path.isfile(message_queue_shutdown_file_path)):
        logger.error(MESSAGE_QUEUE_SHUTDOWN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(message_queue_shutdown_file_path))
        return False    
    # Shutting down message queue
    logger.info(SHUTTING_DOWN_MESSAGE_QUEUE_INFO_MESSAGE)
    installation_lock.acquire()
    try:
        shut_down_success = (0 == run_bash_scipt(message_queue_shutdown_file_path))
    finally:            
        installation_lock.release()     
    if shut_down_success:
        logger.info(SHUTTING_DOWN_MESSAGE_QUEUE_INFO_MESSAGE)
    else:
        logger.error(MESSAGE_QUEUE_SHUTDOWN_FAILED_ERROR_MESSAGE)
    return shut_down_success

def get_message_queue(message_queue_context,
                      callback               =   None, 
                      message_queue_type     =   None,
                      host                   =   None,
                      port                   =   None):
    message_queue_type  = message_queue_type if message_queue_type else DEFAULT_MESSAGE_QUEUE
    message_queue       = load_message_queue(callback, message_queue_context, message_queue_type, host, port)
    return message_queue

def run_message_queue(message_queue_context,
                      callback               =   None, 
                      message_queue_type     =   None,
                      host                   =   None,
                      port                   =   None):
    message_queue = get_message_queue(message_queue_context, callback, message_queue_type, host, port)
    # If message queue - run it
    if message_queue:
        return message_queue.run()
    