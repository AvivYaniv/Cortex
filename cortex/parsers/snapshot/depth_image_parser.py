import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class DepthImageParser:
    
    field = 'depth_image'
    
    def parse(self, context, snapshot):
        matplotlib.use('Agg')
        path = context.path('depth_image.jpg')
        image = np.mat(snapshot.depth_image.data)
        image = image.reshape(snapshot.depth_image.width, snapshot.depth_image.height)
        plt.imsave(path, image, cmap='hot')
        