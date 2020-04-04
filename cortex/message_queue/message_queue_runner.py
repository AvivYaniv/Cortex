import os 

from cortex.utils import DynamicModuleLoader

import logging
from cortex.logger import LoggerLoader
from cortex.message_queue.rabbitmq_mq import RabbitMQMessageQueue

# Log loading
logger_loader             = LoggerLoader()
logger_loader.load_log_config()
logger                    = logging.getLogger(__name__)

# Error messages
MESSAGE_QUEUE_TYPE_NOT_FOUND_ERROR  =   'Specified message queue class not found in directory'

def load_message_queue(message_queue_type):
    LOOKUP_TOKEN        =   'MessageQueue'
    NAME_IDENTIFIER     =   'name'
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
    _, class_mqs = \
        DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, LOOKUP_TOKEN, NAME_IDENTIFIER)
    if message_queue_type not in class_mqs:
        logger.critical(MESSAGE_QUEUE_TYPE_NOT_FOUND_ERROR)
        return None
    # Returning specified message queue object
    return class_mqs[message_queue_type](logger)

def run_message_queue(message_queue_type=RabbitMQMessageQueue.name):
    message_queue = load_message_queue(message_queue_type)
    # If message queue not found - exit
    if not message_queue:
        return
    # Else, message queue found - run
    else:
        message_queue.run()
    