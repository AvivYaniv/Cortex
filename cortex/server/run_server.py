
from cortex.server.server_service import run_server_service

def run_server(host='', port='', publish=None):
    """Starts a server to which snapshots can be uploaded with `cortex.client.upload_sample`"""
    run_server_service(host, port, publish)
    