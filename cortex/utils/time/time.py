
import datetime
from builtins import staticmethod

DATETIME_FORMAT             = '%Y-%m-%d_%H-%M-%S-%f'

class TimeUtils:
    
    EPOCH_MOMENT            = datetime.datetime.utcfromtimestamp(0)

    @staticmethod
    def unix_time_millis(dt):
        return int((dt - TimeUtils.EPOCH_MOMENT).total_seconds() * 1000.0)
    
    @staticmethod
    def get_time_stamp(dt, datetime_format=None):
        datetime_format = datetime_format if datetime_format else DATETIME_FORMAT
        return dt.strftime(datetime_format)
