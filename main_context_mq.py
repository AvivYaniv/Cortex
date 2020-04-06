
from cortex.readers.dictionary import DictionayReaderDriver

from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

FILENAME = 'cortex/publisher_consumer/message_queue/context/rabbitmq_config.yaml'

if "__main__" == __name__:
    dictionary_reader_driver = DictionayReaderDriver.find_driver(FILENAME)
    if not dictionary_reader_driver:
        print('File driver not found!')     
    try:
        with open(FILENAME, 'rt') as f:
            dictionary = dictionary_reader_driver(f) 
            
            kw = { 'name' : 'color_parser' }
            
            mq_context_factory  =   MessageQueueContextFactory('rabbitmq')
            ctx                 =   mq_context_factory.get_mq_context('parser', 'publishers', 'parsed_snapshot', name='color_parser')
            
            print(ctx)
            
            x = 1
            x = x + 1
    except Exception as e:
        print(f'Parsing error : {e}')
