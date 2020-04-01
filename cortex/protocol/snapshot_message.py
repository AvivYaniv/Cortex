from datetime import datetime

from cortex.sample import ColorImage
from cortex.sample import DepthImage

class SnapshotMessage:
    DATETIME_FORMAT         = '%Y-%m-%d_%H-%M-%S-%f'
    CONCISE_DATE_FORMAT     = '%d %B, %Y'
    CONCISE_HOUR_FORMAT     = '%H:%M:%S.%f'
    
    def __init__(self, snapshot, fields):
        self.timestamp		= snapshot.timestamp
        self.datetime       = snapshot.datetime
        # If not presented - setting default values
        if 'translation' not in fields:
            self.snapshot.translation = (0.0, 0.0, 0.0)
        else:
            self.translation    = snapshot.translation
        if 'rotation' not in fields:
            self.rotation = (0.0, 0.0, 0.0, 0.0)
        else:
            self.rotation       = snapshot.rotation
        if 'color_image' not in fields:
            self.color_image = ColorImage()
        else:
            self.color_image    = snapshot.color_image
        if 'depth_image' not in fields:
            self.depth_image = DepthImage() 
        else:
            self.depth_image    = snapshot.depth_image
        if 'user_feeling' not in fields:
            self.user_feeling = (0.0, 0.0, 0.0, 0.0)       
        else:
            self.user_feeling   = snapshot.user_feeling

    def __repr__(self):
        return f'Snapshot(datetime={datetime.strftime(self.datetime, SnapshotMessage.DATETIME_FORMAT)}, translation={self.translation}, rotation={self.rotation}, color_image={self.color_image}, depth_image={self.depth_image})'
    
    def __str__(self):
        return f'Snapshot from {datetime.strftime(self.datetime, SnapshotMessage.CONCISE_DATE_FORMAT)} at {datetime.strftime(self.datetime, SnapshotMessage.CONCISE_HOUR_FORMAT)} on {self.translation} / {self.rotation} with a {self.color_image} and a {self.depth_image}'
    