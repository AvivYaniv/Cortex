
from cortex.database.database_runner import load_database 

# TODO : Replace with real code
class _DataBase:
    def __init__(self, database_type, host, port):
        self.driver     = load_database(database_type, host, port)
    def create_entity(self, entity_name, **kwargs):
        return self.driver.create_entity(entity_name, **kwargs)
    def get_entity(self, entity_name, **kwargs):
        entity = self.driver.get_entity(entity_name, **kwargs)
        if entity is None:
            raise LookupError()
        return entity
    def update_entity(self, entity_name, entity_id, **kwargs):
        self.driver.update_entity(entity_name, entity_id, **kwargs)
