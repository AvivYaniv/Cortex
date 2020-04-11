
import sys
import inspect

from cortex.utils import strip_dictionary_fields_whitelist

from cortex.api.marshal import JSONMarshal
from cortex.api.marshal import marshalLoader

from cortex.database.database_cortex import _DataBaseCortex

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

class APIService:
    # Constants Section
    DEFAULT_MARSHAL_FORMAT          = JSONMarshal.type
    # Constructor Section
    def __init__(self, database_type=None, database_host=None, database_port=None, marshal_format=None):
        # DataBase
        self.database_type          = database_type 
        self.database_host          = database_host
        self.database_port          = database_port
        self._database              = _DataBaseCortex(self.database_type, self.database_host, self.database_port)
        # Output Formatter
        self.marshal_format         = marshal_format if marshal_format else APIService.DEFAULT_MARSHAL_FORMAT
        self._marshal_loader        = marshalLoader(self.marshal_format)
    # Methods Section
    def prepare_get_query_result(self, dictionary, approved_fields_for_display=[]):
        strip_dictionary_fields_whitelist(dictionary, approved_fields_for_display)
        return self._marshal_loader.marshal(dictionary)
    def get_all_users(self):
        users                       = self._database.get_all_users()
        # TODO : CONVERT TO OUTPUT FORMAT
        approved_fields_for_display = [ 'user_id' , 'username' ]
        return [self.prepare_get_query_result(user, approved_fields_for_display) for user in users]
    def get_user(self, user_id):
        user                        = self._database.get_user(user_id=user_id)
        # TODO : CONVERT TO OUTPUT FORMAT
        approved_fields_for_display = [ 'user_id' , 'username', 'birth_date', 'gender' ]
        return self.prepare_get_query_result(user, approved_fields_for_display)
    def get_snapshots(self, user_id):
        snapshots                   = self._database.get_all_snapshots(user_id=user_id)
        # TODO : CONVERT TO OUTPUT FORMAT
        approved_fields_for_display = [ 'snapshot_uuid' , 'timestamp' ]
        return [self.prepare_get_query_result(snapshot, approved_fields_for_display) for snapshot in snapshots]
    
    