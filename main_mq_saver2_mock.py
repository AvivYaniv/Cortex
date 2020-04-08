from pathlib import Path

import threading

from cortex.publisher_consumer.message_queue.consumer.Message_queue_consumer_thread import MessageQueueConsumerThread
    
def get_filename(fpath):
    return Path(fpath).stem

def get_saver_number(s):
    return [c for c in s if c.isdigit()][0]

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
        
class Saver:
    def __init__(self):
        self.database           = _DataBaseMock()
        self.saver_number       = get_saver_number(get_filename(__file__))
        self.saver_name         = 'saver.' + self.saver_number
        self.saving_callback    = self.publish_parsed_callback()
        self.lock               = threading.Lock()
        
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
        parser1_listener = self.create_listen_thread('parser.1')
        parser2_listener = self.create_listen_thread('parser.2')
        parser1_listener.start()
        parser2_listener.start()
        
    def create_listen_thread(self, parser_name):
        return MessageQueueConsumerThread(callback      =   self.saving_callback, 
                                          caller_type   =   'saver', 
                                          category      =   'consumers', 
                                          item          =   parser_name)
    
if "__main__" == __name__:
    saver = Saver()
    saver.run()
    