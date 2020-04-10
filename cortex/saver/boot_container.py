from cortex.saver.saver_service import run_saver_service

from cortex.envvars import get_database_parameters
from cortex.envvars import get_message_queue_parameters

def run_saver_container():
    database_type, database_host, database_port                 = get_database_parameters()
    message_queue_type, message_queue_host, message_queue_port  = get_message_queue_parameters()
    run_saver_service(database_type, database_host, database_port, message_queue_type, message_queue_host, message_queue_port)

if "__main__" == __name__:
    run_saver_container()
    