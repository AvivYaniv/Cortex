
from datetime import datetime

from cortex.database.database_cortex import _DataBaseCortex

from cortex.publisher_consumer.messages import MessageQueueMessages, MessageQueueMessagesTyeps

import logging
from cortex.logger import _LoggerLoader
from cortex.utils.json.json import json_to_object

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

class SaverMessagesHandler:
    DEFAULT_ENCODING            =   'utf-8'
    
    def __init__(self, database_type, database_host, database_port):
        # DataBase
        self.database_type          = database_type 
        self.database_host          = database_host
        self.database_port          = database_port
        self._database              = _DataBaseCortex(self.database_type, self.database_host, self.database_port)
        # Messages
        self.messages               = MessageQueueMessages() 
        # Save methods
        self.SAVE_METHODS           =                       \
            {                                               \
                'pose'          : self.save_parsed_pose,    \
                'user_feelings' : self.save_user_feelings,  \
                'color_image'   : self.save_color_image,    \
                'depth_image'   : self.save_depth_image,    \
            }
    # Message Handling Methods    
    def handle(self, message):
        message                 = message if isinstance(message, str) else message.decode(SaverMessagesHandler.DEFAULT_ENCODING)
        parsed_snapshot_message = self.messages.get_message(                              \
                    MessageQueueMessagesTyeps.PARSED_SNAPSHOT_MESSAGE).deserialize(message)
        # Fetch user id and path
        user_info               = parsed_snapshot_message.user_info        
        self.save_user(user_info)
        self.save_snapshot(parsed_snapshot_message.snapshot_uuid, user_info.user_id, parsed_snapshot_message.snapshot_timestamp)
        # Fetch parsed field
        field                   = parsed_snapshot_message.field
        snapshot_uuid           = parsed_snapshot_message.snapshot_uuid
        result                  = parsed_snapshot_message.result
        is_uri                  = parsed_snapshot_message.is_uri
        self.save_parsed(field, snapshot_uuid, result, is_uri)
    # Save Methods
    def save_parsed(self, field, snapshot_uuid, result, is_uri):
        if field not in self.SAVE_METHODS.keys():
            logger.error(f'saving field {field} is unknown')
            return
        self.SAVE_METHODS[field](snapshot_uuid, result, is_uri)
    # User Saving Method
    def save_user(self, user_info):
        if self._database.has_user(user_id=user_info.user_id):
            return
        user_id         = user_info.user_id
        username        = user_info.username
        birth_date      = datetime.fromtimestamp(user_info.birth_date)
        gender          = user_info.gender
        creation_status =                                   \
            self._database.create_user(                     \
                user_id    = user_id,                       \
                username   = username,                      \
                birth_date = birth_date,                    \
                gender     = gender,                        \
                )
        if creation_status:
            logger.info(f'user {user_id} added successfully!')
        else:
            logger.error(f'failed to add user {user_id}')
    # Snapshot Saving Method
    def save_snapshot(self, snapshot_uuid, user_id, snapshot_timestamp):
        if self._database.has_snapshot(snapshot_uuid=snapshot_uuid):
            return
        creation_status =                                   \
            self._database.create_snapshot(                 \
                snapshot_uuid = snapshot_uuid,              \
                user_id       = user_id,                    \
                timestamp     = snapshot_timestamp          \
                )
        if creation_status:
            logger.info(f'snapshot {snapshot_uuid} added successfully!')
        else:
            logger.error(f'failed to add snapshot {snapshot_uuid}')    
    # Fields Saving Methods
    def save_parsed_pose(self, snapshot_uuid, result, is_uri):
        snapshot_uuid   = snapshot_uuid
        pose            = json_to_object(result)
        creation_status =                                       \
            self._database.create_pose(                         \
                snapshot_uuid  = snapshot_uuid,                 \
                translation_x  = pose.translation.x,            \
                translation_y  = pose.translation.y,            \
                translation_z  = pose.translation.z,            \
                rotation_x     = pose.rotation.x,               \
                rotation_y     = pose.rotation.y,               \
                rotation_z     = pose.rotation.z,               \
                rotation_w     = pose.rotation.w,               \
                )
        if creation_status:
            logger.info(f'pose of snapshot {snapshot_uuid} added successfully!')
        else:
            logger.error(f'failed to add pose of snapshot {snapshot_uuid}')
    def save_user_feelings(self, snapshot_uuid, result, is_uri):
        snapshot_uuid   = snapshot_uuid
        user_feelings   = json_to_object(result)
        creation_status =                                       \
            self._database.create_user_feelings(                \
                snapshot_uuid  = snapshot_uuid,                 \
                hunger         = user_feelings.hunger,          \
                thirst         = user_feelings.thirst,          \
                exhaustion     = user_feelings.exhaustion,      \
                happiness         = user_feelings.happiness,    \
                )
        if creation_status:
            logger.info(f'user_feelings of snapshot {snapshot_uuid} added successfully!')
        else:
            logger.error(f'failed to add user_feelings of snapshot {snapshot_uuid}')
    def save_color_image(self, snapshot_uuid, result, is_uri):
        snapshot_uuid   = snapshot_uuid
        uri             = result
        creation_status =                                       \
            self._database.create_color_image(                  \
                snapshot_uuid  = snapshot_uuid,                 \
                uri            = uri,                           \
                )
        if creation_status:
            logger.info(f'color_image of snapshot {snapshot_uuid} added successfully!')
        else:
            logger.error(f'failed to add color_image of snapshot {snapshot_uuid}')    
    def save_depth_image(self, snapshot_uuid, result, is_uri):
        snapshot_uuid   = snapshot_uuid
        uri             = result
        creation_status =                                       \
            self._database.create_depth_image(                  \
                snapshot_uuid  = snapshot_uuid,                 \
                uri            = uri,                           \
                )
        if creation_status:
            logger.info(f'depth_image of snapshot {snapshot_uuid} added successfully!')
        else:
            logger.error(f'failed to add depth_image of snapshot {snapshot_uuid}') 
            