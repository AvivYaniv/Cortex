from cortex.publisher_consumer.messages.json import *

class MessageQueueMessagesTyeps:
    RAW_SNAPSHOT_MESSAGE       = 0
    PARSED_SNAPSHOT_MESSAGE    = 1
    
class MessageQueueMessagesTypes:
    JSON_MESSAGES_TYPE          = 0
    
class MessageQueueMessages:
    JSON_MESSAGES                   =                                                           \
        {                                                                                       \
            MessageQueueMessagesTyeps.RAW_SNAPSHOT_MESSAGE      : RawSnapshotMessageJson,       \
            MessageQueueMessagesTyeps.PARSED_SNAPSHOT_MESSAGE   : ParsedSnapshotMessageJson,    \
        }
    
    MESSAGE_QUEUE_MESSAGES_TABLE    =                                                           \
        {                                                                                       \
            MessageQueueMessagesTypes.JSON_MESSAGES_TYPE   : JSON_MESSAGES,                     \
        }
    
    def __init__(self, messages_type=MessageQueueMessagesTypes.JSON_MESSAGES_TYPE):
        self.message_queue_messages = MessageQueueMessages.MESSAGE_QUEUE_MESSAGES_TABLE[messages_type]
        
    def get_message(self, message_type):
        return self.message_queue_messages[message_type]
        