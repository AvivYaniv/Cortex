
from flask import Flask
from flask import request
from flask import send_file
from flask_restful import Api, Resource
from cortex.api.api_service import APIService

from cortex.api.api_urls import *

# RESTful Flask
app = Flask(__name__)
api = Api(app)

# API Service
api_service = None

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

def get_result_data_uri(user_id, snapshot_uuid, result_name):
    host_url = request.host
    def get_result_data_uri_with_host(user_id, snapshot_uuid, result_name):
        return get_api_url(API_URL_FORMAT_GET_RESULT_DATA, host=f'http://{host_url}')        
    return get_result_data_uri_with_host(user_id, snapshot_uuid, result_name)
    
class ResultAPI(Resource):
    def get(self, user_id, snapshot_uuid, result_name):
        return api_service.get_result(user_id, snapshot_uuid, result_name, data_uri_converter=get_result_data_uri)

class ResultDataAPI(Resource):
    def get(self, user_id, snapshot_uuid, result_name):
        uri     =   api_service.get_result_data(user_id, snapshot_uuid, result_name)
        return send_file(uri)

class SnapshotResultsAPI(Resource):
    def get(self, user_id, snapshot_uuid):
        return api_service.get_snapshot_results(user_id, snapshot_uuid, data_uri_converter=get_result_data_uri)

class UserSnapshotsResultsAPI(Resource):
    def get(self, user_id):
        return api_service.get_user_results(user_id, data_uri_converter=get_result_data_uri)

# Embedding Dictionaries Section
DICT_FLASK    = {                                                   \
                  '%user_id%'       : '<int:user_id>',              \
                  '%snapshot_uuid%' : '<string:snapshot_uuid>',     \
                  '%result_name%'   : '<string:result_name>',       \
                }

def get_flask_api_url(api_url_format):
    return get_custom_api_url(api_url_format, DICT_FLASK)

# Adding API Resources
# User API Section
api.add_resource(AllUsersAPI,               get_flask_api_url(API_URL_FORMAT_GET_ALL_USERS),                    endpoint = 'users'                  )
api.add_resource(UserAPI,                   get_flask_api_url(API_URL_FORMAT_GET_USER),                         endpoint = 'user'                   )
# Snapshot API Section
api.add_resource(UserSnapshotsAPI,          get_flask_api_url(API_URL_FORMAT_GET_ALL_USER_SNAPSHOTS),           endpoint = 'snapshots'              )
api.add_resource(SnapshotAPI,               get_flask_api_url(API_URL_FORMAT_GET_USER_SNAPSHOT),                endpoint = 'snapshot'               )
# Result API Section
api.add_resource(ResultAPI,                 get_flask_api_url(API_URL_FORMAT_GET_RESULT),                       endpoint = 'result'                 )
api.add_resource(ResultDataAPI,             get_flask_api_url(API_URL_FORMAT_GET_RESULT_DATA),                  endpoint = 'result_data'            )
# Snapshot results API Section
api.add_resource(SnapshotResultsAPI,        get_flask_api_url(API_URL_FORMAT_GET_SNAPSHOT_RESULTS),             endpoint = 'snapshot_results'       )
api.add_resource(UserSnapshotsResultsAPI,   get_flask_api_url(API_URL_FORMAT_GET_ALL_USER_RESULTS),             endpoint = 'user_snapshot_results'  )

def run_api(host=None, port=None, database_type=None, database_host=None, database_port=None):
    """Starts an API server of which users and snapshots can be retrived"""
    # Parse server address
    api_server_host                         = host      if host else DEFAULT_API_HOST
    api_server_port                         = int(host  if host else DEFAULT_API_PORT)    
    global api_service
    api_service = APIService(database_type, database_host, database_port)
    app.run(api_server_host, api_server_port)
