# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.publisher_consumer.message_queue import MessageQueuePublisher 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

if "__main__" == __name__:
    mq_context_factory      =   MessageQueueContextFactory()
    message_queue_context   =   mq_context_factory.get_mq_context('server', 'publishers', 'snapshots')
    message_queue_publisher =   MessageQueuePublisher(message_queue_context)
    publish_function        =   message_queue_publisher.run()
    
    for i in range(10):
        publish_function(message=f'Server message {i}', publisher_name='snapshot')
    
    print("Server sent message!")
    