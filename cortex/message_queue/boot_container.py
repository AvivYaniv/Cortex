from cortex.message_queue import run_message_queue

import os

# Constants Section
MESSAGE_QUEUE_ENVIRONMENT_VARIABLE                  =   'TYPE'      

# Messages Section
BOOTING_MESSAGE_QUEUE_INFO_MESSAGE                  =   'Booting message queue...'

def run_message_queue_command(message_queue_type):
        # If message queue type not specified, activating default 
        if not message_queue_type:            
            run_message_queue()
        # Else, message queue specified, activating it 
        else:
            run_message_queue(message_queue_type)

if "__main__" == __name__:
    message_queue_type = None
    
    # Validating container has been specified
    if MESSAGE_QUEUE_ENVIRONMENT_VARIABLE in os.environ:
        message_queue_type = os.environ[MESSAGE_QUEUE_ENVIRONMENT_VARIABLE]
    
    # Booting message queue
    print(BOOTING_MESSAGE_QUEUE_INFO_MESSAGE)
    run_message_queue_command(message_queue_type)
    