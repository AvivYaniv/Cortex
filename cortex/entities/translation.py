
class Translation:
    def __init__(self, translation):
        self.x, self.y, self.z = translation

    def clear(self):
        self.x, self.y, self.z = (0.0, 0.0, 0.0)

    def get(self):
        return self.x, self.y, self.z
            