
from cortex.server.server_service import run_server

def run_server(host='', port='', publish=None):
    """Starts a server to which snapshots can be uploaded with `upload_sample`"""  
    server_service = run_server(host, port, publish)
    server_service.run()
