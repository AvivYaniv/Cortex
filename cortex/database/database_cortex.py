from cortex.database.database_base import _DataBaseBase

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
    ENTITY_USER            =   'user'
    ENTITY_SNAPSHOT        =   'snapshot'
    ENTITY_POSE            =   'pose'
    ENTITY_USER_FEELINGS   =   'user_feelings'
    ENTITY_COLOR_IMAGE     =   'color_image'
    ENTITY_DEPTH_IMAGE     =   'depth_image'

    ENTITY_IDS_NAMES       =    { ENTITY_USER : 'user_id', ENTITY_SNAPSHOT : 'snapshot_uuid' }

    PARSED_ENTITIES_LIST   =    [ ENTITY_POSE, ENTITY_USER_FEELINGS, ENTITY_COLOR_IMAGE, ENTITY_DEPTH_IMAGE ]

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
    def get_user(self, *, user_id):
        user =                                                                     \
            self.driver.get_entity(                                                \
                _DataBaseCortex.ENTITY_USER,                                       \
                user_id=user_id                                                    \
                )
        if user is None:
            logger.error('user {user_id} not found!')
        return user
    def update_user(self, *, user_id, **kwargs):
        update_result =                                                             \
            self.driver.update_entity(                                              \
                _DataBaseCortex.ENTITY_USER,                                        \
                _DataBaseCortex.ENTITY_IDS_NAMES[_DataBaseCortex.ENTITY_USER],      \
                user_id,                                                            \
                **kwargs                                                            \
                ) 
        if not update_result:
            logger.error('error while updating user {user_id} to {kwargs_to_string(**kwargs)}')
    # Snapshot Entity Section
    def create_snapshot(self, *, snapshot_uuid, snapshotname, birth_date, gender):
        return                                                                      \
            self.driver.create_entity(                                              \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                snapshot_uuid=snapshot_uuid,                                        \
                snapshotname=snapshotname,                                          \
                birth_date=birth_date,                                              \
                gender=gender                                                       \
                )
    def get_snapshot(self, *, snapshot_uuid):
        snapshot =                                                                  \
            self.driver.get_entity(                                                 \
                _DataBaseCortex.ENTITY_SNAPSHOT,                                    \
                snapshot_uuid=snapshot_uuid                                         \
                )
        if snapshot is None:
            logger.error('snapshot {snapshot_uuid} not found!')
        return snapshot
    