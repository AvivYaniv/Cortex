from struct import pack, unpack, calcsize
from datetime import datetime

from .serialization import Serialization

from .depthimage import DepthImage
from .colorimage import ColorImage

class Snapshot:
    ERROR_DATA_INCOMPLETE   = 'incomplete data'

    DATETIME_FORMAT         = 'YYYY-mm-dd_HH-MM-SS-fffff'

    SERIALIZATION_ENDIANITY = '<'

    SERIALIZATION_HEADER    = 'Qddddddd'
    SERIALIZATION_BODY      = '{0}{1}'
    SERIALIZATION_TRAILER   = 'ffff'
    SERIALIZATION_FORMAT    = SERIALIZATION_ENDIANITY + SERIALIZATION_HEADER + SERIALIZATION_BODY + SERIALIZATION_TRAILER
    
    def __init__(self, datetime, translation, rotation, color_image, depth_image, user_feeling):
        self.datetime       = datetime
        self.translation    = translation
        self.rotation       = rotation
        self.color_image    = color_image
        self.depth_image    = depth_image
        self.user_feeling   = user_feeling
         
    def __repr__(self):
        return f'Snapshot(datetime={datetime.strftime(self.datetime, Snapshot.DATETIME_FORMAT)}, translation={self.translation}, rotation={self.rotation}, color_image={self.color_image}, depth_image={self.depth_image})'
    
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
        return                                              \
            pack(self.get_current_serialization_format(),   \
                 self.datetime,                             \
                 self.translation,                          \
                 self.rotation,                             \
                 self.color_image.serialize(),              \
                 self.depth_image.serialize(),              \
                 self.user_feeling)
    
    @staticmethod
    def deserialize(*, stream):
        header_size                                         =   calcsize(Snapshot.SERIALIZATION_HEADER)
        data_header                                         =   stream.read(header_size)
        
        if data_header is None:
            raise EOFError()
        
        timestamp, t_x, t_y, t_z, r_x, r_y, r_z, r_w    =   \
            unpack(Snapshot.SERIALIZATION_HEADER, data_header)
        
        translation, rotation                               =   \
            (t_x, t_y, t_z), (r_x, r_y, r_z, r_w)
        
        color_image                                         =   ColorImage.deserialize(stream=stream)  
        color_image.save_image(str(timestamp)+'_color.png')      
        depth_image                                         =   DepthImage.deserialize(stream=stream)
        depth_image.save_image(str(timestamp)+'_depth.png') 
        
        trailer_size                                        =   calcsize(Snapshot.SERIALIZATION_TRAILER)
        data_trailer                                        =   stream.read(trailer_size)
         
        if data_trailer is None:
            raise RuntimeError(Snapshot.ERROR_DATA_INCOMPLETE)
         
        (hunger, thirst, exhaustion, happiness)             =   \
            unpack(Snapshot.SERIALIZATION_ENDIANITY + Snapshot.SERIALIZATION_TRAILER, data_trailer)
         
        user_feeling                                        =   \
            (hunger, thirst, exhaustion, happiness)
        
        return Snapshot(datetime.fromtimestamp(timestamp/1000.0), translation, rotation, color_image, depth_image, user_feeling)
    