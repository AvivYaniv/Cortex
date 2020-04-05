from cortex.publisher_consumer.message_queue import MessageQueuePublisher, MessageQueueContext 

if "__main__" == __name__:
    message_queue_context =                 \
        MessageQueueContext(                \
            exchange_type  = 'fanout',      \
            exchange_name  = 'raw',         \
            queue_name     = '',            \
            binding_keys   = None           \
            )
    
    message_queue_publisher = MessageQueuePublisher(message_queue_context)
    publish_function        = message_queue_publisher.run()
    
    for i in range(10):
        publish_function(message=f'Server message {i}', routing_key='snapshot')
    
    print("Server sent message!")
    