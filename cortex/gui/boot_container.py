from cortex.gui.gui_server import run_server

from cortex.envvars import get_ipaddress_parameters
from cortex.envvars import get_api_parameters

def run_gui_container():
    host, port                                                  = get_ipaddress_parameters()
    api_host, api_port                                          = get_api_parameters()    
    run_server(host='', port='', api_host='', api_port='')

if "__main__" == __name__:
    run_gui_container()
    