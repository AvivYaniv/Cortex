import io

from datetime import datetime
from struct import pack, calcsize
import time

from cortex.utils import Serialization

from cortex.entities import Snapshot

from cortex.sample.depthimage import DepthImage
from cortex.sample.colorimage import ColorImage

from ..snapshot import SnapshotMessage

class SnapshotMessageNative(SnapshotMessage):
    ERROR_DATA_INCOMPLETE   = 'incomplete data'

    DATETIME_FORMAT         = '%Y-%m-%d_%H-%M-%S-%f'
    CONCISE_DATE_FORMAT     = '%d %B, %Y'
    CONCISE_HOUR_FORMAT     = '%H:%M:%S.%f'

    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'Qddddddd'
    SERIALIZATION_TRAILER   = 'ffff'
    
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
            self._current_serialization_format = SnapshotMessageNative.SERIALIZATION_FORMAT.format(raw_color_image_format, raw_depth_image_format) 
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        header =                                                                                                \
            pack(SnapshotMessageNative.SERIALIZATION_ENDIANITY + SnapshotMessageNative.SERIALIZATION_HEADER,    \
                 self.timestamp,                                                                                \
                 *self.translation,                                                                             \
                 *self.rotation)    
        
        body =                                                                                                  \
            self.color_image.serialize() + self.depth_image.serialize()    
        
        trailer =                                                                                               \
            pack(SnapshotMessageNative.SERIALIZATION_ENDIANITY + SnapshotMessageNative.SERIALIZATION_TRAILER,   \
                 *self.user_feeling)
        
        return header + body + trailer
    
    @staticmethod
    def read(data):
        
        stream = io.BytesIO(data)
        
        timestamp, t_x, t_y, t_z, r_x, r_y, r_z, r_w        =   \
            Serialization.read(stream, SnapshotMessageNative.SERIALIZATION_HEADER, expect_eof=True)
        
        translation, rotation                               =   \
            (t_x, t_y, t_z), (r_x, r_y, r_z, r_w)
        
        color_image                                         =   ColorImage.read(stream)
        
        # TODO DEBUG REMOVE
        # color_image.save_image(str(timestamp)+'_color_image.png')  
        depth_image                                         =   DepthImage.read(stream)
        # TODO DEBUG REMOVE
        # depth_image.save_image(str(timestamp)+'_depth_image.png')
        
        (hunger, thirst, exhaustion, happiness)             =   \
            Serialization.read(stream, SnapshotMessageNative.SERIALIZATION_TRAILER)
         
        user_feeling                                        =   \
            (hunger, thirst, exhaustion, happiness)
        
        return Snapshot(timestamp, translation, rotation, color_image, depth_image, user_feeling)
    