import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import warnings

import io

class DepthImageParser:
    
    field       =   'depth_image'
    
    extension   =   '.png'
    
    def parse(self, snapshot):
        matplotlib.use('Agg')
        warnings.filterwarnings('ignore', category=PendingDeprecationWarning)
        image               = np.mat(snapshot.depth_image.data)
        warnings.filterwarnings('default', category=PendingDeprecationWarning)
        image               = image.reshape(snapshot.depth_image.width, snapshot.depth_image.height)
        plt.imshow(image, cmap='hot')
        plt.axis('off')
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        image_byte_array    = io.BytesIO()
        plt.savefig(image_byte_array, format='PNG')        
        return image_byte_array.getvalue()
    