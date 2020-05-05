
from cortex.utils import strip_dictionary_fields_whitelist
from cortex.utils import strip_dictionary_fields_blacklist

from cortex.api.marshal import JSONMarshal
from cortex.api.marshal import marshalLoader

from cortex.database.database_cortex import _DataBaseCortex

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Decorators Section
def function_logging_decorator(fn):
    def func(*a, **kw):
        logger.info('%s(%s, %s)', fn.__name__, a, kw)
        return fn(*a, **kw)
    return func

class APIService:
    # Constants Section
    DEFAULT_MARSHAL_FORMAT                                  = JSONMarshal.type
    DATA_URI_KEY_NAME                                       = 'data_uri'
    EMPTY_RESULT                                            = ''
    # Constructor Section
    def __init__(self, database_type=None, database_host=None, database_port=None, marshal_format=None):
        # DataBase        
        self._database                                      = _DataBaseCortex(database_type, database_host, database_port)
        # Output Formatter
        self.marshal_format                                 = marshal_format if marshal_format else APIService.DEFAULT_MARSHAL_FORMAT
        self._marshal_loader                                = marshalLoader(self.marshal_format)
    # Methods Section
    # Representation Methods Section
    def _prepare_get_query_result_for_reperesentation(self, dictionary):
        return self._marshal_loader.marshal(dictionary)
    def _prepare_get_query_result_whitelist(self, dictionary, approved_fields_for_display=[]):
        strip_dictionary_fields_whitelist(dictionary, approved_fields_for_display)
        return self._prepare_get_query_result_for_reperesentation(dictionary)
    def _prepare_get_query_result_blacklist(self, dictionary, disapproved_fields_for_display=[]):
        strip_dictionary_fields_blacklist(dictionary, disapproved_fields_for_display)
        return self._prepare_get_query_result_for_reperesentation(dictionary)
    # CRUD Methods Section
    @function_logging_decorator
    def get_all_users(self):
        users                                               = self._database.get_all_users()
        approved_fields_for_display                         = [ 'user_id' , 'username' ]
        return [self._prepare_get_query_result_whitelist(user, approved_fields_for_display) for user in users]
    @function_logging_decorator
    def get_user(self, user_id):
        user                                                = self._database.get_user(user_id=user_id)
        approved_fields_for_display                         = [ 'user_id' , 'username', 'birth_date', 'gender' ]
        return self._prepare_get_query_result_whitelist(user, approved_fields_for_display)
    @function_logging_decorator
    def get_user_snapshots(self, user_id):
        snapshots                                           = self._database.get_user_snapshots(user_id=user_id)
        approved_fields_for_display                         = [ 'snapshot_uuid' , 'datetime' ]
        return [self._prepare_get_query_result_whitelist(snapshot, approved_fields_for_display) for snapshot in snapshots]
    @function_logging_decorator
    def get_snapshot(self, user_id, snapshot_uuid):
        snapshot                                            = self._database.get_snapshot_details(user_id=user_id, snapshot_uuid=snapshot_uuid)
        approved_fields_for_display                         = [ 'snapshot_uuid' , 'datetime', self._database.AVAILABLE_RESULTS_LIST_NAME ]
        return self._prepare_get_query_result_whitelist(snapshot, approved_fields_for_display)
    @staticmethod
    def embed_data_uri(result, user_id, snapshot_uuid, result_name, data_uri_converter=None):
        if result and data_uri_converter:
            result[APIService.DATA_URI_KEY_NAME]    = data_uri_converter(user_id, snapshot_uuid, result_name)
    @function_logging_decorator
    def get_snapshot_results(self, user_id, snapshot_uuid, data_uri_converter=None):
        snapshot                                            = self._database.get_snapshot_details(user_id=user_id, snapshot_uuid=snapshot_uuid)
        for parsed_entity_name in snapshot[self._database.AVAILABLE_RESULTS_LIST_NAME]:
            snapshot[parsed_entity_name] = self.get_result(user_id, snapshot_uuid, parsed_entity_name, data_uri_converter)
        approved_fields_for_display                         = [ 'snapshot_uuid' , 'datetime']
        approved_fields_for_display.extend(self._database.PARSED_ENTITIES_LIST)
        return self._prepare_get_query_result_whitelist(snapshot, approved_fields_for_display)
    @function_logging_decorator
    def get_user_results(self, user_id, data_uri_converter=None):
        user_results = []
        for snapshot in self._database.get_user_snapshots(user_id=user_id):
            user_results.append(self.get_snapshot_results(user_id, snapshot['snapshot_uuid'], data_uri_converter))
        return user_results
    @function_logging_decorator
    def get_result(self, user_id, snapshot_uuid, result_name, data_uri_converter=None):
        text_retrieval_method                               =   self._database.get_text_retrieval_method(result_name)
        if text_retrieval_method:
            result                                          =   text_retrieval_method(snapshot_uuid=snapshot_uuid)
            disapproved_fields_for_display                  =   [ 'snapshot_uuid' ]
        else:
            binary_retrieval_method                         =   self._database.get_binary_retrieval_method(result_name)
            if binary_retrieval_method:
                result                                      =   binary_retrieval_method(snapshot_uuid=snapshot_uuid)
                disapproved_fields_for_display              =   [ 'snapshot_uuid', 'uri' ]
                APIService.embed_data_uri(result, user_id, snapshot_uuid, result_name, data_uri_converter)                
        if text_retrieval_method or binary_retrieval_method:             
            return self._prepare_get_query_result_blacklist(result, disapproved_fields_for_display)
        return APIService.EMPTY_RESULT
    @function_logging_decorator
    def get_result_data(self, user_id, snapshot_uuid, result_name):
        binary_retrieval_method                     =   self._database.get_binary_retrieval_method(result_name)
        if binary_retrieval_method:
            result                                  =   binary_retrieval_method(snapshot_uuid=snapshot_uuid)
            uri                                     =   result['uri']
            return uri
        return APIService.EMPTY_RESULT 
    
       