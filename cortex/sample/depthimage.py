import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from .snapshotimage import SnapshotImage

class DepthImage(SnapshotImage):
    PIXEL_SERIALIZATION_FORMAT = 'f'
    PIXEL_ELEMENTS_COUNT       = 1
    
    def __init__(self, height=0, width=0, image=[]):
        super().__init__(height, width, image, DepthImage.PIXEL_SERIALIZATION_FORMAT, DepthImage.PIXEL_ELEMENTS_COUNT)
         
    def __repr__(self):
        return f'<Image: depth {self.height}x{self.width}>'
    
    def __str__(self):
        return f'{self.height}x{self.width} depth image'
    
    def _parse_image(self):
        matplotlib.use('Agg')
        W = np.mat(self.image)
        W = W.reshape(self.width, self.height)
        self._image_file = W
        
    def _save_file(self, file_name):
        plt.imsave(file_name, self._image_file, cmap='hot')
        
    @staticmethod
    def deserialize(*, stream):
        image =                                                                                     \
            SnapshotImage.deserialize(                                                              \
                                stream=stream,                                                      \
                                pixel_serialization_format=DepthImage.PIXEL_SERIALIZATION_FORMAT,   \
                                pixel_elements_count=DepthImage.PIXEL_ELEMENTS_COUNT) 
        image.__class__ = DepthImage        
        return image
        