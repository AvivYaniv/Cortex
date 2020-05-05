import os 

# Constants Section
API_HOST_ENVIRONMENT_VARIABLE             =   'API_HOST'
API_PORT_ENVIRONMENT_VARIABLE             =   'API_PORT'

def get_api_parameters():
    api_host                = None
    api_port                = None
    # Setting non-default host if specified
    if API_HOST_ENVIRONMENT_VARIABLE in os.environ:
        api_host = os.environ[API_HOST_ENVIRONMENT_VARIABLE]
    # Setting non-default port if specified
    if API_PORT_ENVIRONMENT_VARIABLE in os.environ:
        api_port = os.environ[API_PORT_ENVIRONMENT_VARIABLE]
    return api_host, api_port
