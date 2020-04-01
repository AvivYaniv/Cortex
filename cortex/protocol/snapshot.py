import io

from cortex.sample import Snapshot

from cortex.sample import ColorImage
from cortex.sample import DepthImage

class SnapshotMessage:
    def __init__(self, snapshot, fields):
        # If not presented - setting default values
        if 'translation' not in fields:
            snapshot.translation = (0.0, 0.0, 0.0)
        if 'rotation' not in fields:
            snapshot.rotation = (0.0, 0.0, 0.0, 0.0)
        if 'color_image' not in fields:
            snapshot.color_image = ColorImage()
        if 'depth_image' not in fields:
            snapshot.depth_image = DepthImage() 
        if 'user_feeling' not in fields:
            snapshot.user_feeling = (0.0, 0.0, 0.0, 0.0)       
        # Setting values
        self.snapshot = snapshot
        
    def serialize(self):
        return self.snapshot.serialize()
    
    @staticmethod
    def read(data):
        return Snapshot.read(io.BytesIO(data))
    