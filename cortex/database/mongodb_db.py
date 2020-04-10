
import pymongo

from cortex.utils.json import kwargs_to_json

from cortex.database.database_driver import _DataBaseDriver

class MongoDBDataBase(_DataBaseDriver):
    
    name            = 'mongodb'

    # Constructor Section
    def __init__(self, logger, host, port):
        super().__init__(logger, host, port)
        self._client = pymongo.MongoClient(host, port)
        self._db     = self._client.db    
    # CRUD Methods Section
    def create_entity(self, entity_name, **kwargs):
        entity_document = self._db[entity_name]
        result          = entity_document.insert_one(kwargs_to_json(**kwargs)) 
        return result
    def get_entity(self, entity_name, **kwargs):
        entity = self.driver.get_entity(entity_name, **kwargs)
        if entity is None:
            raise LookupError()
        return entity
    def update_entity(self, entity_name, entity_id, **kwargs):
        self.driver.update_entity(entity_name, entity_id, **kwargs)
    # Run Method
    def run(self):
        # MongoDB ''tables'' (BSON documents) are creates on demand
        # therefore, no need to initialize it on the code
        pass
    