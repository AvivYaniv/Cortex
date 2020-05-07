
from cortex.envvars import get_message_queue_parameters
from cortex.publisher_consumer.message_queue.message_queue_runner import install_message_queue

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

if "__main__" == __name__:
    message_queue_type, message_queue_host, message_queue_port  = get_message_queue_parameters()
    install_message_queue(message_queue_type)
    logger.info('MessageQueue is ready to handle messages!')
    # Keep Running
    while True:
        pass
    