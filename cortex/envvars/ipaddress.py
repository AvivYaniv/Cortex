import os 

# Constants Section
HOST_ENVIRONMENT_VARIABLE             =   'HOST'
PORT_ENVIRONMENT_VARIABLE             =   'PORT'

def get_ipaddress_parameters():
    host                = None
    port                = None
    # Setting non-default host if specified
    if HOST_ENVIRONMENT_VARIABLE in os.environ:
        host = os.environ[HOST_ENVIRONMENT_VARIABLE]
    # Setting non-default port if specified
    if PORT_ENVIRONMENT_VARIABLE in os.environ:
        port = os.environ[PORT_ENVIRONMENT_VARIABLE]
    return host, port
