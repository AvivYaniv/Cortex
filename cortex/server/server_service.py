import threading

from cortex.utils import Listener

from cortex.server.server_handler import ServerHandler

from cortex.publisher_consumer.message_queue import MessageQueuePublisherThread 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
# Networking
DEFAULT_HOST            =    '127.0.0.1'
DEFAULT_PORT            =    '8000'

class ServerService:
    lock                        = threading.Lock()
    
    # Constructor Section
    def __init__(self, host='', port='', publish=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        # Default parameter resolution
        self.server_ip_str      = host if host else DEFAULT_HOST
        self.server_port_int    = int(port if port else DEFAULT_PORT)
        # Setting snapshot publish function
        self._set_publish_snapshot_function(publish, message_queue_type, message_queue_host, message_queue_port)
    # Methods Section
    # Publish Methods Section
    # Generates callback with custom arguments - by this currying function 
    def publish_mq_callback(self, publish_function, **kwargs):
        def mq_publish(message):
            self.lock.acquire()
            try:
                publish_function(message, **kwargs)
            finally:            
                self.lock.release()
        return mq_publish
    # Setting publish snapshot function
    def _set_publish_snapshot_function(self, publish=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        # If publish function has been passed
        if publish:
            # Setting publish function
            self.publish_snapshot_function = publish
            # Returning, no need to initiate message-queue
            return
        # Initializing Message Queue
        self._init_mq(message_queue_type, message_queue_host, message_queue_port)
        # Setting Message Queue snapshot publish function
        self.mq_publish_snapshot_function   =   self.message_queue_publisher.get_publish_function()
        self.publish_snapshot_function      =   self.publish_mq_callback(self.mq_publish_snapshot_function, publisher_name='snapshot')
        self.message_queue_publisher.run()
    # Message Queue Methods Section
    # Initialize MessageQueue and set publish function     
    def _init_mq(self, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        # No publish function has been passed, initializing message queue
        mq_context_factory              =   MessageQueueContextFactory(message_queue_type)
        message_queue_context           =   mq_context_factory.get_mq_context('server', 'publishers', 'snapshots')
        self.message_queue_publisher    =   \
            MessageQueuePublisherThread(    \
            message_queue_context,          \
            message_queue_type,             \
            message_queue_host,             \
            message_queue_port              \
            )        
    # Core Logic Method Section  
    # Run server service and handle clients
    def run(self):
        # Logging initialization
        logger.info(f'starting server on {self.server_ip_str}:{self.server_port_int}')
        while True:
            # Listening to incoming messages and handling them accordingly
            with Listener(self.server_port_int, self.server_ip_str) as listener:
                # Accept client        
                connection = listener.accept()        
                # Initialize client ServerHandler
                handler = ServerHandler(connection, self.publish_snapshot_function)        
                # Handle client
                handler.start()

def run_server_service(host='', port='', publish=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
    """Starts a server to which snapshots can be uploaded with `upload_sample`"""  
    server_service = ServerService(host, port, publish, message_queue_type, message_queue_host, message_queue_port)
    server_service.run()
    