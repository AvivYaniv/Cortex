from cortex.publisher_consumer.message_queue import MessageQueueConsumer, MessageQueueContext 

def callback(message):
    print(" [x] Received %r" % message)

if "__main__" == __name__:
    message_queue_context =                 \
        MessageQueueContext(                \
            exchange_type  = 'direct',      \
            exchange_name  = '',            \
            queue_name     = 'hello',       \
            binding_keys   = None           \
            )
    
    message_queue_consumer = MessageQueueConsumer(callback, message_queue_context)
    message_queue_consumer.run()
    