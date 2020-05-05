from cortex.api.api_server import run_api

from cortex.envvars import get_ipaddress_parameters
from cortex.envvars import get_database_parameters

def run_api_container():
    host, port                                                  = get_ipaddress_parameters()
    database_type, database_host, database_port                 = get_database_parameters()    
    api_service = run_api(host, port, database_type, database_host, database_port)
    api_service.run()

if "__main__" == __name__:
    run_api_container()
    