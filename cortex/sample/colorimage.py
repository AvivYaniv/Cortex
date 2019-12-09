from PIL import Image

from .snapshotimage import SnapshotImage

class ColorImage(SnapshotImage):
    PIXEL_SERIALIZATION_FORMAT = 'B'
    PIXEL_ELEMENTS_COUNT       = 3
    
    def __init__(self, height=0, width=0, image=[]):
        super().__init__(height, width, image, ColorImage.PIXEL_SERIALIZATION_FORMAT, ColorImage.PIXEL_ELEMENTS_COUNT)
         
    def __repr__(self):
        return f'<Image: color {self.height}x{self.width}>'
    
    def __str__(self):
        return f'{self.height}x{self.width} color image'
    
    def _parse_image(self):
        if (0 != len(self.image) % self.pixel_elements_count):
            raise RuntimeError(SnapshotImage.ERROR_DATA_INCOMPLETE)
    
        self._image_file    = Image.new('RGB', (self.width, self.height))
        pixels              = self._image_file.load()
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = (y * self.width + x) * self.pixel_elements_count
                B, G, R = self.image[pos:pos+self.pixel_elements_count]
                pixels[x, y] = (R, G, B)
                
    def _save_file(self, file_name):
        self._image_file.save(file_name)

    @staticmethod
    def deserialize(*, stream):
        image =                                                                                     \
            SnapshotImage.deserialize(                                                              \
                                stream=stream,                                                      \
                                pixel_serialization_format=ColorImage.PIXEL_SERIALIZATION_FORMAT,   \
                                pixel_elements_count=ColorImage.PIXEL_ELEMENTS_COUNT)
        
        # TODO: Due to bug in hardware these are swapped during serialization 
        image.height, image.width = image.width, image.height 
        
        image.__class__ = ColorImage        
        return image
        