import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class DepthImageParser:
    
    field       = 'depth_image'
    
    extension   =   '.jpg'
    
    def parse(self, parser_saver, context, snapshot, path=None):
        matplotlib.use('Agg')
        path = path if path else parser_saver.get_path(context, extension=DepthImageParser.extension)
        parser_saver.create_path(path)
        image = np.mat(snapshot.depth_image.data)
        image = image.reshape(snapshot.depth_image.width, snapshot.depth_image.height)
        plt.imsave(path, image, cmap='hot')
        return path
    