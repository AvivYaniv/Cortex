
from cortex.utils.url import parse_url

from cortex.api.api_server import run_api

def run_api_server(host, port, db_url=None):
    """Starts a api server which serves API requests""" 
    database_type=None
    database_host=None
    database_port=None 
    if db_url:
        database_type, database_host, database_port  =   \
            parse_url(db_url)    
    api_service = run_api(host, port, database_type, database_host, database_port)
    api_service.run()
