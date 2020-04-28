from cortex.database.database_base import _DataBaseBase

from cortex.utils import TimeUtils
from cortex.utils import kwargs_to_string

import logging
from cortex.logger import _LoggerLoader

# Log loading
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

class _DataBaseCortex(_DataBaseBase):
    # Constants Section
    # Entities
    ENTITY_USER                         =   'user'
    ENTITY_SNAPSHOT                     =   'snapshot'
    
    ENTITY_POSE                         =   'pose'
    ENTITY_USER_FEELINGS                =   'user_feelings'
    ENTITY_COLOR_IMAGE                  =   'color_image'
    ENTITY_DEPTH_IMAGE                  =   'depth_image'

    AVAILABLE_RESULTS_LIST_NAME         =   'aviable_results'

    ENTITY_IDS_NAMES                    =   { ENTITY_USER : 'user_id', ENTITY_SNAPSHOT : 'snapshot_uuid' }

    PARSED_ENTITIES_LIST                =   [ ENTITY_POSE, ENTITY_USER_FEELINGS, ENTITY_COLOR_IMAGE, ENTITY_DEPTH_IMAGE ]

    # Methods Section    
    # User Entity Section
    def create_user(self, *, user_id, username, birth_date, gender):
        return                                                                     \
            self.driver.create_entity(                                             \
                _DataBaseCortex.ENTITY_USER,                                       \
                user_id=user_id,                                                   \
                username=username,                                                 \
                birth_date=birth_date,                                             \
                gender=gender                                                      \
                )
    def has_user(self, *, user_id):
        is_exist =                                                                  \
            self.driver.has_entity(                                                 \
                _DataBaseCortex.ENTITY_USER,                                        \
                user_id=user_id                                                     \
                )
        return is_exist
    def get_user(self, *, user_id):
        user =                                                                     \
            self.driver.get_entity(                                                \
                _DataBaseCortex.ENTITY_USER,                                       \
                user_id=user_id                                                    \
                )
        if user is None:
            logger.warning('user {user_id} not found!')
        return user
    def get_all_users(self):
        users =                                                                     \
            self.driver.get_entities(                                               \
                _DataBaseCortex.ENTITY_USER                                         \
                )
        if users is None:
            logger.warning('no users found!')
        return users
    def update_user(self, *, user_id, **kwargs):
        update_result =                                                             \
            self.driver.update_entity(                                              \
                _DataBaseCortex.ENTITY_USER,                                        \
                _DataBaseCortex.ENTITY_IDS_NAMES[_DataBaseCortex.ENTITY_USER],      \
                user_id=user_id,                                                    \
                **kwargs                                                            \
                ) 
        if not update_result:
            logger.warning('error while updating user {user_id} to {kwargs_to_string(**kwargs)}')
    # Snapshot Entity Section
    def create_snapshot(self, *, snapshot_uuid, user_id, timestamp):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                snapshot_uuid=snapshot_uuid,                                        \
                user_id=user_id,                                                    \
                timestamp=timestamp,                                                \
                datetime=TimeUtils.milliseconds_timestamp_to_dateime(timestamp),    \
                )
    def has_snapshot(self, *, snapshot_uuid):
        is_exist =                                                                  \
            self.driver.has_entity(                                                 \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                snapshot_uuid=snapshot_uuid                                         \
                )
        return is_exist
    def get_snapshot(self, *, snapshot_uuid):
        snapshot =                                                                  \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if snapshot is None:
            logger.warning('snapshot {snapshot_uuid} not found!')
        return snapshot
    def get_user_snapshots(self, *, user_id):
        snapshots =                                                                 \
            self.driver.get_entities(                                               \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                user_id=user_id                                                     \
                )
        if snapshots is None:
            logger.warning('user {user_id} snapshots not found!')
        return snapshots
    def get_snapshot_details(self, *, user_id, snapshot_uuid):
        snapshot =                                                                  \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                user_id=user_id,                                                    \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if snapshot is None:
            logger.warning('snapshot {snapshot_uuid} not found!')
        # Adding available results to snapshot details
        snapshot.update( { _DataBaseCortex.AVAILABLE_RESULTS_LIST_NAME : [] } )
        for parsed_entity_name in _DataBaseCortex.PARSED_ENTITIES_LIST:
            if self.driver.has_entity(parsed_entity_name):
                snapshot[_DataBaseCortex.AVAILABLE_RESULTS_LIST_NAME].append(parsed_entity_name)
        return snapshot
    def remove_entity_ids(self, entity):
        for entity_id in self.ENTITY_IDS_NAMES.values():
            entity.pop(entity_id, None)  
    # Pose Entity Section
    def create_pose(self, *,            \
                    snapshot_uuid,      \
                    translation_x,      \
                    translation_y,      \
                    translation_z,      \
                    rotation_x,         \
                    rotation_y,         \
                    rotation_z,         \
                    rotation_w,         \
                    ):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_POSE,                                        \
                snapshot_uuid   = snapshot_uuid,                                    \
                translation_x   = translation_x,                                    \
                translation_y   = translation_y,                                    \
                translation_z   = translation_z,                                    \
                rotation_x      = rotation_x,                                       \
                rotation_y      = rotation_y,                                       \
                rotation_z      = rotation_z,                                       \
                rotation_w      = rotation_w,                                       \
                )
    def get_pose(self, *, snapshot_uuid):
        pose =                                                                      \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_POSE,                                        \
                snapshot_uuid=snapshot_uuid,                                        \
                )
        if pose is None:
            logger.warning('pose for snapshot {snapshot_uuid} not found!')
        return pose
    # User Feelings Entity Section
    def create_user_feelings(self, *,   \
                    snapshot_uuid,      \
                    hunger,             \
                    thirst,             \
                    exhaustion,         \
                    happiness,          \
                    ):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_USER_FEELINGS,                               \
                snapshot_uuid   = snapshot_uuid,                                    \
                hunger          = hunger,                                           \
                thirst          = thirst,                                           \
                exhaustion      = exhaustion,                                       \
                happiness       = happiness,                                        \
                )
    def get_user_feelings(self, *, snapshot_uuid):
        user_feelings =                                                             \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_USER_FEELINGS,                               \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if user_feelings is None:
            logger.warning('user feelings for snapshot {snapshot_uuid} not found!')
        return user_feelings
    # User Color Image Entity Section
    def create_color_image(self, *,     \
                    snapshot_uuid,      \
                    uri,                \
                    width,              \
                    height              \
                    ):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_COLOR_IMAGE,                                 \
                snapshot_uuid   = snapshot_uuid,                                    \
                uri             = uri,                                              \
                width           = width,                                            \
                height          = height                                            \
                )
    def get_color_image(self, *, snapshot_uuid):
        color_image =                                                               \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_COLOR_IMAGE,                                 \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if color_image is None:
            logger.warning('color image for snapshot {snapshot_uuid} not found!')
        return color_image
    # User Depth Image Entity Section
    def create_depth_image(self, *,     \
                    snapshot_uuid,      \
                    uri,                \
                    width,              \
                    height              \
                    ):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_DEPTH_IMAGE,                                 \
                snapshot_uuid   = snapshot_uuid,                                    \
                uri             = uri,                                              \
                width           = width,                                            \
                height          = height                                            \
                )
    def get_depth_image(self, *, snapshot_uuid):
        depth_image =                                                               \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_DEPTH_IMAGE,                                 \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if depth_image is None:
            logger.warning('depth image for snapshot {snapshot_uuid} not found!')
        return depth_image
    # Retrieval Methods Section
    def get_text_retrieval_method(self, parsed_field_name):
        PARSED_TEXT_RETRIEVAL_FUNCTIONS     =    {  _DataBaseCortex.ENTITY_POSE         : self.get_pose,        _DataBaseCortex.ENTITY_USER_FEELINGS    : self.get_user_feelings    }
        if parsed_field_name in PARSED_TEXT_RETRIEVAL_FUNCTIONS.keys():
            return PARSED_TEXT_RETRIEVAL_FUNCTIONS[parsed_field_name]
        return None
    def get_binary_retrieval_method(self, parsed_field_name):
        PARSED_BINARY_RETRIEVAL_FUNCTIONS   =    {  _DataBaseCortex.ENTITY_COLOR_IMAGE  : self.get_color_image, _DataBaseCortex.ENTITY_DEPTH_IMAGE      : self.get_depth_image      }
        if parsed_field_name in PARSED_BINARY_RETRIEVAL_FUNCTIONS.keys():
            return PARSED_BINARY_RETRIEVAL_FUNCTIONS[parsed_field_name]
        return None
    # 