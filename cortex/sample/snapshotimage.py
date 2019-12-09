from PIL import Image
from struct import pack, unpack, calcsize

from .serialization import Serialization

class SnapshotImage:
    ERROR_DATA_INCOMPLETE        = 'incomplete data'

    SERIALIZATION_ENDIANITY      = '<'

    SERIALIZATION_HEADER         = 'II'
    
    def __init__(self, height, width, image, pixel_serialization_format, pixel_elements_count):
        self.image                                 = image
        self.width, self.height                    = width, height
        self.pixel_serialization_format            = pixel_serialization_format
        self.pixel_elements_count                  = pixel_elements_count
        SnapshotImage.SERIALIZATION_PAYLOAD_FORMAT = '{0}' + self.pixel_serialization_format 
        SnapshotImage.SERIALIZATION_FORMAT         = SnapshotImage.SERIALIZATION_ENDIANITY + SnapshotImage.SERIALIZATION_HEADER + SnapshotImage.SERIALIZATION_PAYLOAD_FORMAT
         
    def __repr__(self):
        return f'SnapshotImage(height={self.height}, width={self.width})'
    
    def save_image(self, file_name):
        if not hasattr(self, '_image_file'):
            self._parse_image()
        self._save_file(file_name)
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):
            image_size          = self.width * self.height
            pixel_array_size    = image_size * calcsize(self.pixel_serialization_format) * self.pixel_elements_count
            
            # height         :    uint32
            # width          :    uint32
            # data           :    [array]
            self._current_serialization_format =    \
                SnapshotImage.SERIALIZATION_FORMAT.format(pixel_array_size) 
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        # If image is empty
        if not self.image:
            return                                              \
                pack(self.get_current_serialization_format(),   \
                     self.height,                               \
                     self.width)
        # Image is non-empty
        return                                              \
            pack(self.get_current_serialization_format(),   \
                 self.height,                               \
                 self.width,                                \
                 self.image)
    
    @staticmethod
    def deserialize(*, stream, pixel_serialization_format, pixel_elements_count):
        width, height                               = \
            Serialization.deserialize(stream, SnapshotImage.SERIALIZATION_HEADER)
        
        image_size                                  = height * width
        pixel_array_size                            = image_size * pixel_elements_count
        
        image = []
        if 0 != pixel_array_size:
            SERIALIZATION_PAYLOAD_FORMAT            = ('{0}' + pixel_serialization_format).format(pixel_array_size)
            image                                   = \
                Serialization.deserialize(stream, SERIALIZATION_PAYLOAD_FORMAT)
        
        return SnapshotImage(height, width, image, pixel_serialization_format, pixel_elements_count)
    