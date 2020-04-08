import os 

# Constants Section
MESSAGE_QUEUE_ENVIRONMENT_VARIABLE                  =   'MQ'
MESSAGE_QUEUE_HOST_ENVIRONMENT_VARIABLE             =   'MQ_HOST'
MESSAGE_QUEUE_PORT_ENVIRONMENT_VARIABLE             =   'MQ_PORT'

def get_message_queue_parameters():
    host                = None
    port                = None
    message_queue_type  = None
    # Setting non-default host if specified
    if MESSAGE_QUEUE_HOST_ENVIRONMENT_VARIABLE in os.environ:
        host = os.environ[MESSAGE_QUEUE_HOST_ENVIRONMENT_VARIABLE]
    # Setting non-default port if specified
    if MESSAGE_QUEUE_PORT_ENVIRONMENT_VARIABLE in os.environ:
        port = os.environ[MESSAGE_QUEUE_PORT_ENVIRONMENT_VARIABLE]
    # Setting non-default message queue type if specified
    if MESSAGE_QUEUE_ENVIRONMENT_VARIABLE in os.environ:
        message_queue_type = os.environ[MESSAGE_QUEUE_ENVIRONMENT_VARIABLE]
    return message_queue_type, host, port
