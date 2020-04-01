from datetime import datetime

class Snapshot:
    DATETIME_FORMAT         = '%Y-%m-%d_%H-%M-%S-%f'
    
    def __init__(self, timestamp, translation, rotation, color_image, depth_image, user_feeling):
        self.timestamp      = timestamp
        self.datetime       = datetime.fromtimestamp(timestamp/1000.0)
        self.translation    = translation
        self.rotation       = rotation
        self.color_image    = color_image
        self.depth_image    = depth_image
        self.user_feeling   = user_feeling
       
    def getTimeStamp(self):
        return datetime.strftime(self.datetime, Snapshot.DATETIME_FORMAT)
 