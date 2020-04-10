
from cortex.database.mongodb_db import MongoDBDataBase
from cortex.database.database_cortex import _DataBaseCortex

from cortex.publisher_consumer.message_queue.context import MessageQueueContextFactory
from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread

from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps
   
class SaverService:
    SERVICE_TYPE                =   'saver'
    
    DEFAULT_ENCODING            =   'utf-8'
    
    # Constructor Section
    def __init__(self, database_type=None, database_host=None, database_port=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        self.saving_callback    = self.save_parsed_callback()
        # Database
        self.database_type      = database_type 
        self.database_host      = database_host
        self.database_port      = database_port
        self.database           = _DataBaseCortex(self.database_type, self.database_host, self.database_port)
        # Message Queue
        self.message_queue_type = message_queue_type
        self.message_queue_host = message_queue_host
        self.message_queue_port = message_queue_port
        # Messages
        self.messages           = MessageQueueMessages() 
    
    # Save Methods Section    
    # Generates save callback with custom arguments - by this currying function 
    def save_parsed_callback(self):
        def save(message):
            self.save_message(message)                               
        return save
    
    def save_message(self, message):
        print('TODO DEBUG REMOVE Saver got a new message')
        message                 = message if isinstance(message, str) else message.decode(SaverService.DEFAULT_ENCODING)
        parsed_snapshot_message = self.messages.get_message(                              \
                    MessageQueueMessagesTyeps.PARSED_SNAPSHOT_MESSAGE).deserialize(message)
        pass
    
    # Core Logic Method Section
    def run(self):
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
