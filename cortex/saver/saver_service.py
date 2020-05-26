
from cortex.publisher_consumer.message_queue.context import MessageQueueContextFactory
from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread

import cortex.saver.saver_messages_handler as saver_messages_handler

import threading

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

class SaverService:
    """    
    Saver class, runs the micro-service logic

    :ivar SaverService.SERVICE_TYPE: name of the service
    """
    SERVICE_TYPE                    =   'saver'
    
    # Constructor Section
    def __init__(self, database_type=None, database_host=None, database_port=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        """
        Initializes a new saver, which consumes messages from the messages-queue, and saves to the database.
    
        :param database_type: Data base type, if empty - default will be selected.
        :param database_host: Data base host, if empty - default will be selected.
        :param database_port: Data base port, if empty - default will be selected.
        :param message_queue_type: Message queue type, if empty - default will be selected.
        :param message_queue_host: Message queue host, if empty - default will be selected.
        :param message_queue_port: Message queue port, if empty - default will be selected.    
        """
        self.saving_callback        = self.save_parsed_callback()
        # Saver handler
        self.saver_messges_handler  = saver_messages_handler.SaverMessagesHandler(database_type, database_host, database_port)
        # Message Queue
        self.message_queue_type     = message_queue_type
        self.message_queue_host     = message_queue_host
        self.message_queue_port     = message_queue_port
        # Locks
        self._lock                  = threading.Lock()        
    # Save Methods Section    
    # Generates save callback with custom arguments - by this currying function 
    def save_parsed_callback(self):
        """
        Decorator for handling messages from the message queue, in a threadsafe manner (because multiple consumers need to call the handling callback).      
        """
        def save(message):
            """
            Callaback to handle messages by the saver.
        
            :param message: Message to be handles by the saver.    
            """
            self._lock.acquire()
            try:
                return self.handle_message(message)
            finally:            
                self._lock.release()                                           
        return save
    
    def handle_message(self, message):
        """
        Calls saver handler on a given message, which has been consumed from the message-queue.
    
        :param message: Message, which has been consumed from the message-queue.
        """
        return self.saver_messges_handler.handle(message)
        
    # Core Logic Method Section
    def run(self):
        """
        Runs the saver micro-service logic, consuming messages from the message-queue and saving them with saver handler.        
        """
        mq_context_factory      = MessageQueueContextFactory(self.message_queue_type)
        message_queue_category_contexts =                       \
            mq_context_factory.get_mq_category_contexts(        \
                caller_type     =   SaverService.SERVICE_TYPE,  \
                category        =   'consumers')        
        consumers_threads       = self.create_consumers_threads(message_queue_category_contexts)
        for consumer_thread in consumers_threads:
            consumer_thread.start()
      
    # Message Queue Methods Section  
    def create_consumers_threads(self, message_queue_category_contexts):
        """
        Creates all the consumer threads from which the saver has to consume from.
    
        :param message_queue_category_contexts: An array of consumer message-queue contexts for creating each of the messge-queue consumer threads.
        """
        consumer_threads = []
        for message_queue_context in message_queue_category_contexts:
            consumer_thread =                   \
                MessageQueueConsumerThread(     \
                    self.saving_callback,       \
                    message_queue_context,      \
                    self.message_queue_type,    \
                    self.message_queue_host,    \
                    self.message_queue_port,    \
                    )
            consumer_threads.append(consumer_thread)
        return consumer_threads
    
def run_saver_service(database_type=None, database_host=None, database_port=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
    saver_service = SaverService(database_type, database_host, database_port, message_queue_type, message_queue_host, message_queue_port)
    saver_service.run()
