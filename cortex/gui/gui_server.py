
import json
from flask import Flask
import requests
import os
from pathlib import Path

# Constants Section
GUI_CLIENT_FOLDER   = str(Path(os.path.dirname(os.path.realpath(__file__)), 'gui_client'))

# API URLs
# TODO : Embed API host URL
API_URL_USER_INFO_FORMAT    = 'http://localhost:5000/api/v1.0/users/{}'
API_URL_USERS_FORMAT        = 'http://localhost:5000/api/v1.0/users'
API_URL_SNAPSHOTS_FORMAT    = 'http://localhost:5000/api/v1.0/users/{}/results'

# Flask
app     = Flask(__name__, static_url_path='', static_folder=GUI_CLIENT_FOLDER, template_folder=GUI_CLIENT_FOLDER)

def read_client_file(fname, folder=GUI_CLIENT_FOLDER):
    file_path = Path(folder, fname)
    file_exists = Path(file_path).is_file()
    if not file_exists:
        return ''        
    with open(file_path, "r") as file:
        file_content = file.read()
        file.close()
    return file_content

def gui_serever():
    def embed_data_in_page(page, **kwargs):
        embedded_page = page
        for key, value in kwargs.items():
            embedded_page = embedded_page.replace(f'%{key}%', value)
        return embedded_page
                
    def embed_data_in_index(raw_index):
        users_json                  =   requests.get(API_URL_USERS_FORMAT).json()
        users_converted             =   []
        for user_json_string in users_json:
            user_json               =   json.loads(user_json_string)
            user_id                 =   user_json['user_id']
            username                =   user_json['username']
            users_converted.append([f'{username}', f'{user_id}'])        
        index_embedded              =   embed_data_in_page(raw_index, users_converted=str(users_converted))
        return index_embedded
    
    def embed_data_in_snapshots(raw_snapshots, user_id):
        user_snapshots_url          =   API_URL_SNAPSHOTS_FORMAT.format(user_id)
        snapshots_json_as_string    =   requests.get(user_snapshots_url).text    
        snapshots_embedded          =   embed_data_in_page(raw_snapshots, snapshots_data=snapshots_json_as_string)        
        user_info_url               =   API_URL_USER_INFO_FORMAT.format(user_id)
        user_info_json              =   json.loads(requests.get(user_info_url).json())
        snapshots_embedded          =   embed_data_in_page(snapshots_embedded,                              \
                                                           username     =   user_info_json['username'],     \
                                                           user_id      =   str(user_info_json['user_id']), \
                                                           birth_date   =   user_info_json['birth_date'],   \
                                                           gender       =   user_info_json['gender'])
        return snapshots_embedded
    
    # General error handler to disclose actual error code
    @app.errorhandler(Exception)
    def server_error_page(e):
        # TODO Log
        return app.send_static_file('error.html'), 200
    
    @app.route('/')
    def index():        
        raw_index           = read_client_file('index.html')
        embedded_index      = embed_data_in_index(raw_index)          
        return embedded_index, 200        
    
    @app.route('/snapshots/id=<string:user_id>', methods=['POST'])
    def user(user_id):
        raw_snapshots       = read_client_file('snapshots.html')
        embedded_snapshots  = embed_data_in_snapshots(raw_snapshots, user_id)
        return embedded_snapshots, 200        

def run_gui_server(address=None):
    """Starts an GUI server of which users and snapshots can be served to client side in convenient way"""
    gui_serever()
    # Parse server address
    address                         = address if address else 'localhost:8080'
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    app.run(server_ip_str, server_port_int)
   
