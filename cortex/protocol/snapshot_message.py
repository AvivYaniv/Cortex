from datetime import datetime

from cortex.entities import Snapshot

from cortex.sample import ColorImage
from cortex.sample import DepthImage

from cortex.utils import TimeUtils

class SnapshotMessage:
    
    def __init__(self, snapshot, fields):
        # If not presented - setting default values
        if 'translation' not in fields:
            snapshot.pose.translation.clear()
        if 'rotation' not in fields:
            snapshot.pose.rotation.clear()
        if 'color_image' not in fields:
            snapshot.color_image.clear() 
        if 'depth_image' not in fields:
            snapshot.depth_image.clear() 
        if 'user_feeling' not in fields:
            snapshot.user_feelings.clear()
        self.snapshot = snapshot
        
    def __repr__(self):
        return f'Snapshot(datetime={datetime.strftime(self.datetime, TimeUtils.DATETIME_FORMAT)}, translation={self.translation}, rotation={self.rotation}, color_image={self.color_image}, depth_image={self.depth_image})'
    
    def __str__(self):
        return f'Snapshot from {datetime.strftime(self.datetime, TimeUtils.CONCISE_DATE_FORMAT)} at {datetime.strftime(self.datetime, TimeUtils.CONCISE_HOUR_FORMAT)} on {self.translation} / {self.rotation} with a {self.color_image} and a {self.depth_image}'
    