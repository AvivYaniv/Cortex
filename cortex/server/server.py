
from cortex.utils.url import parse_url

from cortex.server.server_service import run_server_service

def run_server(host=None, port=None, mq_url=None):
    """Starts a server to which snapshots can be uploaded with `upload_sample`"""  
    message_queue_type, message_queue_host, message_queue_port  =   \
        parse_url(mq_url)
    server_service = run_server(host, port, message_queue_type, message_queue_host, message_queue_port)
    server_service.run()
