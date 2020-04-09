
from cortex.saver.db import _DataBase

from cortex.publisher_consumer.message_queue.context import MessageQueueContextFactory
from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread
    
class SaverService:
    SERVICE_TYPE                =   'saver'
    
    def __init__(self, database_type=None, database_host=None, database_port=None, message_queue_type=None, message_queue_host=None, message_queue_port=None):
        self.saving_callback    = self.save_parsed_callback()
        # Database
        self.database_type      = database_type
        self.database_host      = database_host
        self.database_port      = database_port
        self.database           = _DataBase(database_type, database_host, database_port)
        # Message Queue
        self.message_queue_type = message_queue_type
        self.message_queue_host = message_queue_host
        self.message_queue_port = message_queue_port
        
    # Generates parse callback with custom arguments - by this currying function 
    def save_parsed_callback(self):
        def save(message):
            # TODO : replace with real code
            print(f'before commit')
            message = message.decode("utf-8") 
            self.database.commit(message)
            print(f'after commit')                   
        return save
    
    def run(self):
        mq_context_factory      = MessageQueueContextFactory(self.message_queue_type)
        message_queue_category_contexts =                       \
            mq_context_factory.get_mq_category_contexts(        \
                caller_type     =   SaverService.SERVICE_TYPE,  \
                category        =   'consumers')        
        consumers_threads       = self.create_consumers_threads(message_queue_category_contexts)
        for consumer_thread in consumers_threads:
            consumer_thread.start()
        
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
