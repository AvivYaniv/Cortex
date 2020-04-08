
from cortex.entities.rotation import Rotation
from cortex.entities.translation import Translation

class Pose:
    def __init__(self, translation, rotation):
        self.rotation       = Rotation(rotation)
        self.translation    = Translation(translation)
