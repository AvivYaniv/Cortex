
from cortex.database.database_cortex import _DataBaseCortex

from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

class SaverMessagesHandler:
    DEFAULT_ENCODING            =   'utf-8'
    
    def __init__(self, database_type, database_host, database_port):
        # DataBase
        self.database_type          = database_type 
        self.database_host          = database_host
        self.database_port          = database_port
        self.database               = _DataBaseCortex(self.database_type, self.database_host, self.database_port)
        # Messages
        self.messages               = MessageQueueMessages() 
    
    def save_user(self, user_info):
        if not self.database.has_user(user_id=user_info.user_id):
            print('TODO DEBUG ADD USER')
        pass
    
    def save_parsed(self, field, snapshot_uuid, result, is_uri):
        pass
    
    def handle(self, message):
        message                 = message if isinstance(message, str) else message.decode(SaverMessagesHandler.DEFAULT_ENCODING)
        parsed_snapshot_message = self.messages.get_message(                              \
                    MessageQueueMessagesTyeps.PARSED_SNAPSHOT_MESSAGE).deserialize(message)
        # Fetch user id and path
        user_info               = parsed_snapshot_message.user_info        
        self.save_user(user_info)
        # Fetch parsed field
        field                   = parsed_snapshot_message.field
        snapshot_uuid           = parsed_snapshot_message.snapshot_uuid
        result                  = parsed_snapshot_message.result
        is_uri                  = parsed_snapshot_message.is_uri
        self.save_parsed(field, snapshot_uuid, result, is_uri)
        
    