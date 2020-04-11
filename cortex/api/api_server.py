
from flask import Flask
from flask_restful import Api, Resource
from cortex.api.api_service import APIService

# Constants Section
API_VERSION =   'v1.0'
API_PREFIX  =   f'/api/{API_VERSION}'

# RESTful Flask
app = Flask(__name__)
api = Api(app)

# API Service
api_service = APIService()

class UsersAPI(Resource):
    def get(self):
        return api_service.get_all_users()

class UserAPI(Resource):
    def get(self, user_id):
        return api_service.get_user(user_id)
    
class SnapshotsAPI(Resource):
    def get(self, user_id):
        return api_service.get_snapshots(user_id)

# Adding API Resources
# User API Section
api.add_resource(UsersAPI,      f'{API_PREFIX}/users',                         endpoint = 'users'     )
api.add_resource(UserAPI,       f'{API_PREFIX}/users/<int:user_id>',           endpoint = 'user'      )
# Snapshot API Section
api.add_resource(SnapshotsAPI,  f'{API_PREFIX}/users/<int:user_id>/snapshots', endpoint = 'snapshots' )

def run_api_server(address=None):
    """Starts an API server of which users and snapshots can be retrived"""
    # Parse server address
    address                         = address if address else 'localhost:5000'
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    app.run(server_ip_str, server_port_int)
   
