
from flask import Flask
from flask import send_file

# Flask
app = Flask(__name__)

def gui_serever():
    @app.route('/')
    def index():
        # Return users
        data_str = "OKKKKK"
        return data_str, 200
    
    @app.route('/users/<int:user_id>')
    def user(user_id):
        # If user ID not found
        if str(user_id) not in CThoughtsFileSystem.getUsersDirs(selected_data_dir):
            return '', 404
        
        # Return user thoughts
        data_str    = CThoughtsFileSystem.getUserThoughtsHTML(selected_data_dir, user_id)
        return data_str, 200

def run_gui_server(address=None):
    """Starts an GUI server of which users and snapshots can be served to client side in convenient way"""
    # Parse server address
    address                         = address if address else 'localhost:8080'
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    app.run(server_ip_str, server_port_int)
   
