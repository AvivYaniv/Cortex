import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from .snapshotimage import SnapshotImage

class DepthImage(SnapshotImage):
    PIXEL_SERIALIZATION_FORMAT = 'f'
    PIXEL_ELEMENTS_COUNT       = 1
    
    def __init__(self, width=0, height=0, data=[]):
        super().__init__(width, height, data, DepthImage.PIXEL_SERIALIZATION_FORMAT, DepthImage.PIXEL_ELEMENTS_COUNT)
         
    def __repr__(self):
        return f'<Image: depth {self.height}x{self.width}>'
    
    def __str__(self):
        return f'{self.height}x{self.width} depth image'
    
    def _parse_image(self):
        matplotlib.use('Agg')
        W = np.mat(self.data)
        W = W.reshape(self.width, self.height)
        self._image_file = W
        
    def _save_file(self, file_name):
        plt.imsave(file_name, self._image_file, cmap='hot')
        
    def _fix_hardware_size(self):
        self.width, self.height = self.height, self.width
        
    @staticmethod
    def read(stream):
        image =                                                                                     \
            SnapshotImage.read(                                                                     \
                                stream=stream,                                                      \
                                pixel_serialization_format=DepthImage.PIXEL_SERIALIZATION_FORMAT,   \
                                pixel_elements_count=DepthImage.PIXEL_ELEMENTS_COUNT) 
        image.__class__ = DepthImage        
        return image
        