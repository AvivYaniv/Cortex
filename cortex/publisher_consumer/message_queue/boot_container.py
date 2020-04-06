from cortex.publisher_consumer.message_queue.message_queue_runner import run_message_queue

import os

# Constants Section
MESSAGE_QUEUE_ENVIRONMENT_VARIABLE                  =   'MQ'
HOST_ENVIRONMENT_VARIABLE                           =   'HOST'

# Messages Section
BOOTING_MESSAGE_QUEUE_INFO_MESSAGE                  =   'Booting message queue...'

def run_message_queue_command(message_queue_type, host):
        # If message queue type not specified, activating default 
        if not message_queue_type:            
            run_message_queue(host=host)
        # Else, message queue specified, activating it 
        else:
            run_message_queue(message_queue_type=message_queue_type, host=host)

if "__main__" == __name__:
    host                = None
    message_queue_type  = None
    
    # Setting non-default message queue type if specified
    if MESSAGE_QUEUE_ENVIRONMENT_VARIABLE in os.environ:
        message_queue_type = os.environ[MESSAGE_QUEUE_ENVIRONMENT_VARIABLE]
    
    # Setting non-default host if specified
    if HOST_ENVIRONMENT_VARIABLE in os.environ:
        host = os.environ[HOST_ENVIRONMENT_VARIABLE]
    
    # Booting message queue
    print(BOOTING_MESSAGE_QUEUE_INFO_MESSAGE)
    run_message_queue_command(message_queue_type, host)
    