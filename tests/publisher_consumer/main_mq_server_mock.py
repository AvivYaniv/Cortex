
from cortex.publisher_consumer.message_queue import MessageQueuePublisherThread 
from cortex.publisher_consumer.message_queue.context.message_queue_context_factory import MessageQueueContextFactory

from tests.test_constants import SERVER_MESSAGES_IDS

def run_server_mock():
    mq_context_factory = MessageQueueContextFactory()
    message_queue_context = mq_context_factory.get_mq_context('server', 'publishers', 'snapshots')
    message_queue_publisher = MessageQueuePublisherThread(message_queue_context)
    publish_function = message_queue_publisher.get_publish_function()
    message_queue_publisher.run()    
    for mesage_id in SERVER_MESSAGES_IDS:
        publish_function(message=f'{mesage_id}', publisher_name='snapshot')    
    print("Server finished!")

if "__main__" == __name__:
    run_server_mock()
    