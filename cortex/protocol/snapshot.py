import io

from ..sample import Snapshot

from ..sample import ColorImage
from ..sample import DepthImage

class SnapshotMessage:
    def __init__(self, snapshot, fields):
        # If not presented - setting default values
        if 'color_image' not in fields:
            snapshot.color_image = ColorImage()
        if 'depth_image' not in fields:
            snapshot.depth_image = DepthImage()
        if 'rotation' not in fields:
            snapshot.rotation = (0.0, 0.0, 0.0, 0.0)
        # Setting values
        self.snapshot = snapshot
        
    def serialize(self):
        return self.snapshot.serialize()
    
    @staticmethod
    def read(data):
        return Snapshot.read(io.BytesIO(data))
    