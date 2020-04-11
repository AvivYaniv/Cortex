
from cortex.utils import TimeUtils

from cortex.entities.pose import Pose
from cortex.entities.user_feelings import UserFeelings

class Snapshot:
    
    def __init__(self, timestamp, translation, rotation, color_image, depth_image, user_feelings):
        self.timestamp      = timestamp
        self.datetime       = TimeUtils.timestamp_to_dateime(timestamp)
        self.pose           = Pose(translation, rotation)
        self.color_image    = color_image
        self.depth_image    = depth_image
        self.user_feelings  = UserFeelings(user_feelings)
       
    def getTimeStamp(self):
        return TimeUtils.get_time_stamp(self.datetime)
 