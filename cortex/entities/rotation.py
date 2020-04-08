
class Rotation:
    def __init__(self, rotation):
        self.x, self.y, self.z, self.w = rotation

    def clear(self):
        self.x, self.y, self.z, self.w = (0.0, 0.0, 0.0, 0.0)
        
    def get(self):
        return self.x, self.y, self.z, self.w
    