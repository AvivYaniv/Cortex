from struct import pack, calcsize

from cortex.utils import Serialization

class SnapshotImage:
    ERROR_DATA_INCOMPLETE        = 'incomplete data'

    SERIALIZATION_ENDIANITY      = '<'

    SERIALIZATION_HEADER         = 'II'
    
    def __init__(self, width, height, data, pixel_serialization_format, pixel_elements_count):
        self.data                                  = data
        self.width, self.height                    = width, height
        self.pixel_serialization_format            = pixel_serialization_format
        self.pixel_elements_count                  = pixel_elements_count
         
    def __repr__(self):
        return f'SnapshotImage(height={self.height}, width={self.width})'
    
    def clear(self):
        self.width  =   0
        self.height =   0
        self.data   =   []
    
    def save_image(self, file_name):
        if not hasattr(self, '_image_file'):
            self._parse_image()
        self._save_file(file_name)
    
    def is_empty(self):
        return not self.data or (0 == self.width) or (0 == self.height)
    
    def get_current_serialization_format(self):
        if not hasattr(self, '_current_serialization_format'):
            # height         :    uint32
            # width          :    uint32
            # data           :    [array]
            self._current_serialization_format      = self.SERIALIZATION_HEADER                
            if not self.is_empty():
                image_size                          = self.width * self.height
                pixel_array_size                    = image_size * self.pixel_elements_count
                SERIALIZATION_PAYLOAD_FORMAT        = ('{0}' + self.pixel_serialization_format).format(pixel_array_size)                
                self._current_serialization_format += SERIALIZATION_PAYLOAD_FORMAT 
        return self._current_serialization_format
    
    def get_serialization_size(self):
        if not hasattr(self, '_serialization_size'):
            self._serialization_size = calcsize(self.get_current_serialization_format())
        return self._serialization_size
    
    def serialize(self):
        # If image is empty
        if self.is_empty():
            return                                              \
                pack(self.get_current_serialization_format(),   \
                     self.width,                                \
                     self.height)
        # Image is non-empty
        return                                              \
            pack(self.get_current_serialization_format(),   \
                 self.width,                                \
                 self.height,                               \
                 *self.data)
    
    @staticmethod
    def read(stream, pixel_serialization_format, pixel_elements_count):
        width, height                               = \
            Serialization.read(stream, SnapshotImage.SERIALIZATION_HEADER)
        
        image_size                                  = width * height
        pixel_array_size                            = image_size * pixel_elements_count
        
        data = []
        if 0 != pixel_array_size:
            SERIALIZATION_PAYLOAD_FORMAT            = ('{0}' + pixel_serialization_format).format(pixel_array_size)
            data                                    = \
                Serialization.read(stream, SERIALIZATION_PAYLOAD_FORMAT)
        
        return SnapshotImage(width, height, data, pixel_serialization_format, pixel_elements_count)
    