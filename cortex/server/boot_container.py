from cortex.server.server_service import run_server_service

from cortex.envvars import get_ipaddress_parameters
from cortex.envvars import get_message_queue_parameters

def run_server():
    host, port = get_ipaddress_parameters()
    message_queue_type, message_queue_host, message_queue_port  = get_message_queue_parameters()
    run_server_service(host, port, message_queue_type, message_queue_host, message_queue_port)

if "__main__" == __name__:
    run_server()
    