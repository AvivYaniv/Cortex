
import json
from flask import Flask
import requests
import os
from pathlib import Path

# Constants Section
GUI_CLIENT_FOLDER   = 'gui_client'

# API URLs
API_URL_USERS       = 'http://localhost:5000/api/v1.0/users'

# Flask
app = Flask(__name__, static_url_path='', static_folder=GUI_CLIENT_FOLDER, template_folder=GUI_CLIENT_FOLDER)

def read_client_file(fname, folder=GUI_CLIENT_FOLDER):
    file_path = Path(os.path.dirname(os.path.realpath(__file__)), folder, fname)
    file_exists = Path(file_path).is_file()
    if not file_exists:
        return ''        
    with open(file_path, "r") as file:
        file_content = file.read()
        file.close()
    return file_content

def gui_serever():
    def embed_data_in_index(raw_index):
        users_json              =   requests.get(API_URL_USERS).json()
        users_converted         =   []
        for user_json_string in users_json:
            user_json   = json.loads(user_json_string)
            user_id     = user_json['user_id']
            username    = user_json['username']
            users_converted.append([f'{username}', f'{user_id}'])
        # return raw_index.format(users_converted=users_converted)
        return raw_index.replace('%users_converted%', str(users_converted))
    
    @app.route('/')
    def index(): 
        raw_index       = read_client_file('index.html')
        embedded_index  = embed_data_in_index(raw_index)          
        return embedded_index, 200
    
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
   
