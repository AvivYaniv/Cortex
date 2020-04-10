
import pymongo

from cortex.utils import kwargs_to_string

from cortex.database.database_driver import _DataBaseDriver

class MongoDBDataBase(_DataBaseDriver):
    
    name                = 'mongodb'
    
    db_instance_name    = 'db'
    
    DEFAULT_DB_ID       = '_id'

    # Constructor Section
    def __init__(self, logger, host, port):
        super().__init__(logger, host, port)
        self._client = pymongo.MongoClient(host, port)
        # TODO DEBUG REMOVE !!! [ START ]
        self._client.drop_database(MongoDBDataBase.db_instance_name)
        # TODO DEBUG REMOVE !!! [ END ]
        self._db     = self._client[MongoDBDataBase.db_instance_name]
    # CRUD Methods Section
    def create_entity(self, entity_name, **kwargs):
        entity_document = self._db[entity_name]
        entity_document.insert_one(kwargs)
        return True
    def get_entity(self, entity_name, **kwargs):
        entity = self._db[entity_name].find_one(kwargs)
        if not entity:
            self._logger.error(f'entity of type {entity_name} which is {kwargs_to_string(**kwargs)} not found!')
        return MongoDBDataBase.to_standard_result_entity(entity)
    def get_entities(self, entity_name, **kwargs):
        entities = [e for e in self.get_entities_lazy(entity_name, **kwargs)]
        return entities
    def get_entities_lazy(self, entity_name, **kwargs):
        cursor = self._db[entity_name].find(kwargs)
        if cursor is None:
            self._logger.error(f'entities of type {entity_name} which are {kwargs_to_string(**kwargs)} not found!')
            return []
        for e in cursor:
            yield MongoDBDataBase.to_standard_result_entity(e)
    def update_entity(self, entity_name, id_name, id_value, **kwargs):
        entity_instance = self._db[entity_name].find_one({id_name : id_value})
        update_id_dict  = {MongoDBDataBase.DEFAULT_DB_ID : entity_instance[MongoDBDataBase.DEFAULT_DB_ID]}
        update_dict     = { '$set' : kwargs }
        result_status   = self._db[entity_name].update_one(update_id_dict, update_dict)
        result_success  = 0 < result_status.matched_count
        if not result_success:
            self._logger.error('error while updating {entity_name} {id_value} to {kwargs_to_string(**kwargs)}')
        return result_success
    # Existence Methods
    def has_entity(self, entity_name, **kwargs):
        try:
            self.get_entity(entity_name, **kwargs)
            return True
        except LookupError:
            return False
    # Result Methods
    @staticmethod
    def to_standard_result_entity(result_entity):
        if not result_entity:
            return None
        result_entity.pop(MongoDBDataBase.DEFAULT_DB_ID, None)
        return result_entity    
    # Run Method
    def _create(self):
        # MongoDB ''tables'' (BSON documents) are creates on demand
        # therefore, no need to initialize it prior of using it
        super()._create()
    