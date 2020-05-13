# Change working directory to main directory
import os
os.chdir('../../../')

from pathlib import Path

import threading

from cortex.publisher_consumer.message_queue.context import MessageQueueContextFactory
from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread

    
def get_filename(fpath):
    return Path(fpath).stem


def get_saver_number(s):
    return [c for c in s if c.isdigit()][0]


class _DataBaseMock:
    _shared_state = {}
     
    def __init__(self):    
        self.__dict__ = self.__class__._shared_state
        self.lock = threading.Lock()
    
    def commit(self, data):
        self.lock.acquire()
        try:
            print(f'Commited : {data}')
        finally:            
            self.lock.release()

        
class Saver:

    def __init__(self):
        self.database = _DataBaseMock()
        self.saver_number = get_saver_number(get_filename(__file__))
        self.saver_name = 'saver.' + self.saver_number
        self.saving_callback = self.publish_parsed_callback()
        self.lock = threading.Lock()
        
    # Generates parse callback with custom arguments - by this currying function 
    def publish_parsed_callback(self):

        def save(message):
            self.lock.acquire()
            try:
                print(f'{self.saver_name} before commit')
                message = message.decode("utf-8") 
                self.database.commit(message)
                print(f'{self.saver_name} after commit')
            finally:            
                self.lock.release()                   

        return save
    
    def run(self):
        mq_context_factory = MessageQueueContextFactory()
        message_queue_category_contexts = \
            mq_context_factory.get_mq_category_contexts(\
                caller_type='saver', \
                category='consumers')        
        parser_listen_threads = self.create_consumers_threads(message_queue_category_contexts)
        for lt in parser_listen_threads:
            lt.start()
        
    def create_consumers_threads(self, message_queue_category_contexts):
        consumer_threads = []
        for message_queue_context in message_queue_category_contexts:
            consumer_thread = \
                MessageQueueConsumerThread(callback=self.saving_callback,
                                           message_queue_context=message_queue_context)
            consumer_threads.append(consumer_thread)
        return consumer_threads

    
if "__main__" == __name__:
    saver = Saver()
    saver.run()
