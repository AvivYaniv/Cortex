from cortex.server import run_server

def run_server_command():
    host, port 		= 	'127.0.0.1', '8000'
    run_server(host, port)

if "__main__" == __name__:
    run_server_command()
	