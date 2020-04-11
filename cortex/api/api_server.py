
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

class AllUsersAPI(Resource):
    def get(self):
        return api_service.get_all_users()

class UserAPI(Resource):
    def get(self, user_id):
        return api_service.get_user(user_id)
    
class UserSnapshotsAPI(Resource):
    def get(self, user_id):
        return api_service.get_user_snapshots(user_id)

class SnapshotAPI(Resource):
    def get(self, user_id, snapshot_uuid):
        return api_service.get_snapshot(user_id, snapshot_uuid)

# Adding API Resources
# User API Section
api.add_resource(AllUsersAPI,       f'{API_PREFIX}/users',                                                  endpoint = 'users'      )
api.add_resource(UserAPI,           f'{API_PREFIX}/users/<int:user_id>',                                    endpoint = 'user'       )
# Snapshot API Section
api.add_resource(UserSnapshotsAPI,  f'{API_PREFIX}/users/<int:user_id>/snapshots',                          endpoint = 'snapshots'  )
api.add_resource(SnapshotAPI,       f'{API_PREFIX}/users/<int:user_id>/snapshots/<string:snapshot_uuid>',   endpoint = 'snapshot'   )

def run_api_server(address=None):
    """Starts an API server of which users and snapshots can be retrived"""
    # Parse server address
    address                         = address if address else 'localhost:5000'
    server_ip_str, server_port_str  = address.split(":")
    server_port_int                 = int(server_port_str)
    app.run(server_ip_str, server_port_int)
   
