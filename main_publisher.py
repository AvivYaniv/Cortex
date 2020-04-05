from cortex.message_queue import MessageQueuePublisher, MessageQueueContext 

if "__main__" == __name__:
    message_queue_context =                 \
        MessageQueueContext(                \
            exchange_type  = 'direct',      \
            exchange_name  = '',            \
            queue_name     = 'hello',       \
            binding_keys   = [ 'hello' ]    \
            )
    
    message_queue_publisher = MessageQueuePublisher(message_queue_context)
    publish_function        = message_queue_publisher.run()
    
    publish_function(message='Hello World!', routing_key='hello')
    publish_function(message='Hello Sabich!', routing_key='hello')
    
    print("Publisher sent message!")
    