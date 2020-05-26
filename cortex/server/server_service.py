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
    """    
    Server Service class, runs the micro-service logic

    :ivar ServerService.lock: lock for publish function multithreading 
    :ivar ServerService.SERVICE_TYPE: name of the service
    """
    lock                = threading.Lock()
    
    SERVICE_TYPE        = 'server'
    
    # Constructor Section
    def __init__(self, host='', port='', publish=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        """
        Creates a server service that publishes messages, either to given function or to a message-queue.
    
        :param host: The server host, if empty - default will be selected.
        :param host: The server port, if empty - default will be selected.
        :param publish: Publish function, to which messages would be published (this disables message-queue publishing).
        :param message_queue_type: Message queue type, if empty - default will be selected.
        :param message_queue_host: Message queue host, if empty - default will be selected.
        :param message_queue_port: Message queue port, if empty - default will be selected.            
        """
        # Default parameter resolution
        self.server_ip_str      = host if host else DEFAULT_HOST
        self.server_port_int    = int(port if port else DEFAULT_PORT)
        # Setting snapshot publish function
        self._set_publish_snapshot_function(publish, message_queue_type, message_queue_host, message_queue_port)
    # Methods Section
    # Publish Methods Section
    # Generates callback with custom arguments - by this currying function 
    def publish_threadsafe_wrapper(self, publish_function, **kwargs):
        """
        Wraps publish function to be threadsafe, used both for costume publish function and for message-queue publish function.
    
        :param publish_function: The publish function to wrap.
        :param kwargs: Key-value arguments to pass to the publish function, when called.                    
        """
        def publish_threadsafe(message):
            self.lock.acquire()
            try:
                publish_function(message, **kwargs)
            finally:            
                self.lock.release()
        return publish_threadsafe
    # Setting publish snapshot function
    def _set_publish_snapshot_function(self, publish=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        """
        Sets the function to call when publishing message, either to given function or to a message-queue.
    
        :param publish: Publish function, to which messages would be published (this disables message-queue publishing).
        :param message_queue_type: Message queue type, if empty - default will be selected.
        :param message_queue_host: Message queue host, if empty - default will be selected.
        :param message_queue_port: Message queue port, if empty - default will be selected.                    
        """
        # If publish function has been passed
        if publish:
            # Setting publish function
            self.publish_snapshot_function = self.publish_threadsafe_wrapper(publish)
            # Returning, no need to initiate message-queue
            return
        # Initializing Message Queue
        self._init_mq(message_queue_type, message_queue_host, message_queue_port)
        # Setting Message Queue snapshot publish function
        self.mq_publish_snapshot_function   =   self.message_queue_publisher.get_publish_function()
        self.publish_snapshot_function      =   self.publish_threadsafe_wrapper(self.mq_publish_snapshot_function, publisher_name='snapshot')
        self.message_queue_publisher.run()
    # Message Queue Methods Section
    # Initialize MessageQueue and set publish function     
    def _init_mq(self, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        """
        Initialize MessageQueue and set publish function.
    
        :param message_queue_type: Message queue type, if empty - default will be selected.
        :param message_queue_host: Message queue host, if empty - default will be selected.
        :param message_queue_port: Message queue port, if empty - default will be selected.                    
        """
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
        """
        Run server micro-service to handle clients.                    
        """
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
    