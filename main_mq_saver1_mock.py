from pathlib import Path

import threading

from cortex.publisher_consumer.message_queue import MessageQueueContext
from cortex.publisher_consumer.message_queue import MessageQueueConsumer 

def get_filename(fpath):
    return Path(fpath).stem

def get_saver_number(str):
    return [s for s in str if s.isdigit()][0]

class _DataBaseMock:
    _shared_state = {}
     
    def __init__(self):    
        self.__dict__   = self.__class__._shared_state
        self.lock       = threading.Lock()
    
    def commit(self, data):
        self.lock.acquire()
        try:
            print(f'Commited : {data}')
        finally:            
            self.lock.release()
  
class ListenThread(threading.Thread):
    # parser_name
    # self.generate_callback()
    def __init__(self, parser_name, callback):
        threading.Thread.__init__(self)
        self.parser_name = parser_name
        self.callback    = callback        
    
    def run(self):
        message_queue_context =                 \
        MessageQueueContext(                    \
            exchange_type  = 'fanout',          \
            exchange_name  = self.parser_name,  \
            queue_name     = 'saver',           \
            binding_keys   = [ 'parser.*' ]     \
            )    
        message_queue_consumer = MessageQueueConsumer(self.callback, message_queue_context)
        message_queue_consumer.run()
        
class Saver:
    def __init__(self):
        self.database           = _DataBaseMock()
        self.saver_number       = get_saver_number(get_filename(__file__))
        self.saver_name         = 'saver.' + self.saver_number
        self.saving_callback    = self.generate_callback()
        self.lock               = threading.Lock()
        
    # Generates parse callback with custom arguments - by this currying function 
    def generate_callback(self):
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
        parser1_listener = self.create_listern_thread('parser.1')
        parser2_listener = self.create_listern_thread('parser.2')
        parser1_listener.start()
        parser2_listener.start()
        
    def create_listern_thread(self, parser_name):
        return ListenThread(parser_name, self.saving_callback)
    
if "__main__" == __name__:
    saver = Saver()
    saver.run()
    