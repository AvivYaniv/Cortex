from datetime import datetime

from cortex.utils import TimeUtils

class Snapshot:
    
    def __init__(self, timestamp, translation, rotation, color_image, depth_image, user_feeling):
        self.timestamp      = timestamp
        self.datetime       = datetime.fromtimestamp(timestamp/1000.0)
        self.translation    = translation
        self.rotation       = rotation
        self.color_image    = color_image
        self.depth_image    = depth_image
        self.user_feeling   = user_feeling
       
    def getTimeStamp(self):
        return TimeUtils.get_time_stamp(self.datetime)
 