from datetime import datetime
from struct import pack, calcsize
import time

from cortex.entities import Snapshot as SnapshotEntity

from cortex.utils import Serialization
from cortex.utils import TimeUtils

from .depthimage import DepthImage
from .colorimage import ColorImage

class Snapshot:
    ERROR_DATA_INCOMPLETE   = 'incomplete data'

    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'Qddddddd'
    SERIALIZATION_TRAILER   = 'ffff'
    
    def __init__(self, timestamp, translation, rotation, color_image, depth_image, user_feeling):
        self.timestamp		= timestamp
        self.datetime       = datetime.fromtimestamp(timestamp/1000.0)
        self.translation    = translation
        self.rotation       = rotation
        self.color_image    = color_image
        self.depth_image    = depth_image
        self.user_feeling   = user_feeling
         
    def __repr__(self):
        return f'Snapshot(datetime={datetime.strftime(self.datetime, TimeUtils.DATETIME_FORMAT)}, translation={self.translation}, rotation={self.rotation}, color_image={self.color_image}, depth_image={self.depth_image})'
    
    def __str__(self):
        return f'Snapshot from {datetime.strftime(self.datetime, TimeUtils.CONCISE_DATE_FORMAT)} at {datetime.strftime(self.datetime, TimeUtils.CONCISE_HOUR_FORMAT)} on {self.translation} / {self.rotation} with a {self.color_image} and a {self.depth_image}'
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):
            raw_color_image_format  = Serialization.remove_endianity(self.color_image.get_current_serialization_format())
            raw_depth_image_format  = Serialization.remove_endianity(self.depth_image.get_current_serialization_format())
            
            # datetime       :    uint64
            # translation    :    uint32 * 3
            # rotation       :    uint32 * 4
            # color image    :    uint32 * 2 + [array]
            # depth image    :    uint32 * 2 + [array]
            # feeling        :    uint32 * 4
            self._current_serialization_format = Snapshot.SERIALIZATION_FORMAT.format(raw_color_image_format, raw_depth_image_format) 
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        header =                                                                    \
            pack(Snapshot.SERIALIZATION_ENDIANITY + Snapshot.SERIALIZATION_HEADER,  \
                 self.timestamp,                                               		\
                 *self.translation,                                                 \
                 *self.rotation)    
        
        body =                                                                      \
            self.color_image.serialize() + self.depth_image.serialize()    
        
        trailer =                                                                   \
            pack(Snapshot.SERIALIZATION_ENDIANITY + Snapshot.SERIALIZATION_TRAILER, \
                 *self.user_feeling)
        
        return header + body + trailer
    
    @staticmethod
    def read(stream):
        timestamp, t_x, t_y, t_z, r_x, r_y, r_z, r_w        =   \
            Serialization.read(stream, Snapshot.SERIALIZATION_HEADER, expect_eof=True)
        
        translation, rotation                               =   \
            (t_x, t_y, t_z), (r_x, r_y, r_z, r_w)
        
        color_image                                         =   ColorImage.read(stream)
        
        depth_image                                         =   DepthImage.read(stream)
        
        (hunger, thirst, exhaustion, happiness)             =   \
            Serialization.read(stream, Snapshot.SERIALIZATION_TRAILER)
         
        user_feeling                                        =   \
            (hunger, thirst, exhaustion, happiness)
        
        return SnapshotEntity(timestamp, translation, rotation, color_image, depth_image, user_feeling)
    