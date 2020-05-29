
import json
from flask import Flask
import requests
import os
from pathlib import Path

from cortex.api.api_urls import *

# Constants Section
GUI_SERVER_HOST             = '127.0.0.1'
GUI_SERVER_PORT             = '8080'

GUI_CLIENT_FOLDER           = str(Path(os.path.dirname(os.path.realpath(__file__)), 'gui_client'))

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Flask
app     = Flask(__name__, static_url_path='', static_folder=GUI_CLIENT_FOLDER, template_folder=GUI_CLIENT_FOLDER)

def read_client_file(fname, folder=GUI_CLIENT_FOLDER):
    """
    Reads a file content to be sent to client.

    :param fname: File name to be read.
    :param folder: Folder to which file belongs to, if not specified - default will be selected.
    """
    file_path = Path(folder, fname)
    file_exists = Path(file_path).is_file()
    if not file_exists:
        return ''        
    with open(file_path, "r") as file:
        file_content = file.read()
        file.close()
    return file_content

def gui_serever():
    """
    Handles requests to GUI server using Flask.    
    """
    def embed_data_in_page(page, **kwargs):
        embedded_page = page
        for key, value in kwargs.items():
            embedded_page = embedded_page.replace(f'%{key}%', value)
        return embedded_page
                
    def embed_data_in_index(raw_index):
        users_url                   =   get_api_url(API_URL_FORMAT_GET_ALL_USERS, api_host_name)
        users_json                  =   requests.get(users_url).json()
        users_converted             =   []        
        for user_json_string in users_json:
            if not user_json_string:
                continue
            user_json               =   json.loads(user_json_string)
            user_id                 =   user_json['user_id']
            username                =   user_json['username']
            users_converted.append([f'{username}', f'{user_id}'])        
        index_embedded              =   embed_data_in_page(raw_index, users_converted=str(users_converted))
        return index_embedded
    
    def embed_data_in_snapshots(raw_snapshots, user_id):
        snapshots_embedded          =   embed_data_in_page(raw_snapshots, snapshots_data_url=f'/results/id={user_id}')         
        user_info_url               =   get_api_url(API_URL_FORMAT_GET_USER, api_host_name).format(user_id)
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
        logger.error(f'Error in GUI, {e}', exc_info=True)
        return app.send_static_file('error.html'), 200
    
    @app.route('/')
    def index():        
        raw_index           = read_client_file('index.html')
        embedded_index      = embed_data_in_index(raw_index)          
        return embedded_index, 200        
    
    @app.route('/results/id=<string:user_id>', methods=['POST', 'GET'])
    def results(user_id):
        user_snapshots_url          =   get_api_url(API_URL_FORMAT_GET_ALL_USER_RESULTS, api_host_name).format(user_id)
        snapshots_json_as_string    =   requests.get(user_snapshots_url).text
        response = app.response_class(
            response=json.dumps(snapshots_json_as_string),
            status=200,
            mimetype='application/json'
        )
        return response
    
    @app.route('/snapshots/id=<string:user_id>', methods=['POST'])
    def user(user_id):
        raw_snapshots       = read_client_file('snapshots.html')
        embedded_snapshots  = embed_data_in_snapshots(raw_snapshots, user_id)
        return embedded_snapshots, 200        

def run_server(host='', port='', api_host='', api_port=''):
    run_gui_server(host, port, api_host, api_port)
    
def run_gui_server(host='', port='', api_host='', api_port=''):
    """Starts an GUI server of which users and snapshots can be served to client side in convenient way"""
    gui_serever()
    host = host if host else GUI_SERVER_HOST
    port = port if port else GUI_SERVER_PORT
    global api_host_name
    api_host_name = build_api_host_name(api_host, api_port)
    # Parse server address    
    app.run(host, int(port))
   
