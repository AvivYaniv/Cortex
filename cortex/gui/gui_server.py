
from flask import Flask
from flask import send_file

# Flask
app = Flask(__name__, static_url_path='', static_folder='gui_client', template_folder='gui_client')

def gui_serever():
    @app.route('/')
    def index():           
        return app.send_static_file('index.html')
    
    @app.route('/users/<int:user_id>')
    def user(user_id):
        pass

def run_gui_server(address=None):
    """Starts an GUI server of which users and snapshots can be served to client side in convenient way"""
    gui_serever()
    # Parse server address
    address                         = address if address else 'localhost:8080'
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    app.run(server_ip_str, server_port_int)
   
