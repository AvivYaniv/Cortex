
import threading

from cortex.publisher_consumer.message_queue.context import MessageQueueContextFactory
from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread

from tests.test_constants import SAVER_MOCK_DEFAULT_IDS

from tests.test_constants import MESSAGE_QUEUE_TEST_HOST

from tests.test_constants import get_message_queue_messages_file_path

from tests._utils.structured_file import StructuredFile

from tests.test_constants import SAVER_SERVICE_TYPE

import ast
        
class Saver:

    def __init__(self, saver_id):
        self.saver_id               = saver_id 
        self.service_type           = SAVER_SERVICE_TYPE   
        self.saver_name             = self.service_type + '.' + self.saver_id
        self.saving_callback        = self.publish_parsed_callback() 
        self.saver_structured_file  = StructuredFile(get_message_queue_messages_file_path(self.service_type))
        self.lock                   = threading.Lock()
        
    # Generates parse callback with custom arguments - by this currying function 
    def publish_parsed_callback(self):
        def save(message):
            self.lock.acquire()
            try:
                message         = message.decode("utf-8")
                content_list    = [ self.saver_id ]
                content_list.extend(ast.literal_eval(message))                
                self.saver_structured_file.append_line(content_list)
            finally:    
                self.lock.release()
        return save
    
    def run(self):
        mq_context_factory              = MessageQueueContextFactory()
        message_queue_category_contexts =                                                       \
            mq_context_factory.get_mq_category_contexts(                                        \
                caller_type             = 'saver',                                              \
                category                = 'consumers')        
        parser_listen_threads = self.create_consumers_threads(message_queue_category_contexts)
        for lt in parser_listen_threads:
            lt.start()
        
    def create_consumers_threads(self, message_queue_category_contexts):
        consumer_threads    = []
        for message_queue_context in message_queue_category_contexts:
            consumer_thread = \
                MessageQueueConsumerThread(callback                 =   self.saving_callback,   \
                                           message_queue_context    =   message_queue_context,  \
                                           host                     =   MESSAGE_QUEUE_TEST_HOST)
            consumer_threads.append(consumer_thread)
        return consumer_threads

    
def run_saver_mock(saver_id=None):
    saver_id = saver_id if saver_id else SAVER_MOCK_DEFAULT_IDS[0]
    saver = Saver(saver_id)
    saver.run()
    
if "__main__" == __name__:
    run_saver_mock()
