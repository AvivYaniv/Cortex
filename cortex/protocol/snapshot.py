from ..sample import Snapshot

from ..sample import ColorImage
from ..sample import DepthImage

class SnapshotMessage:
    def __init__(self, datetime, translation, rotation, color_image=None, depth_image=None, user_feeling=None):
        if not color_image:
            color_image = ColorImage()
        if not depth_image:
            depth_image = DepthImage()
        if not rotation:
            rotation = (0.0, 0.0, 0.0, 0.0)
        self.snapshot = Snapshot(datetime, translation, rotation, color_image, depth_image, user_feeling)
        
    def serialize(self):
        return self.snapshot.serialize()
    
    @staticmethod
    def deserialize(*, stream):
        return Snapshot.deserialize(stream=stream)
    