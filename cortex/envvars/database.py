import os 

# Constants Section
DATABASE_ENVIRONMENT_VARIABLE                  =   'DB'
DATABASE_HOST_ENVIRONMENT_VARIABLE             =   'DB_HOST'
DATABASE_PORT_ENVIRONMENT_VARIABLE             =   'DB_PORT'

def get_database_parameters():
    host                = None
    port                = None
    database_type       = None
    # Setting non-default host if specified
    if DATABASE_HOST_ENVIRONMENT_VARIABLE in os.environ:
        host = os.environ[DATABASE_HOST_ENVIRONMENT_VARIABLE]
    # Setting non-default port if specified
    if DATABASE_PORT_ENVIRONMENT_VARIABLE in os.environ:
        port = os.environ[DATABASE_PORT_ENVIRONMENT_VARIABLE]
    # Setting non-default data base type if specified
    if DATABASE_ENVIRONMENT_VARIABLE in os.environ:
        database_type = os.environ[DATABASE_ENVIRONMENT_VARIABLE]
    return database_type, host, port
