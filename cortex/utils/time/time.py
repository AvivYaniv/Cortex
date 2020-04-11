
from datetime import datetime

class TimeUtils:
    
    DATETIME_FORMAT         = '%Y-%m-%d_%H-%M-%S-%f'
    CONCISE_DATE_FORMAT     = '%d %B, %Y'
    CONCISE_HOUR_FORMAT     = '%H:%M:%S.%f'
    
    EPOCH_MOMENT            = datetime.utcfromtimestamp(0)

    @staticmethod
    def timestamp_to_dateime(timestamp, division=1):
        return datetime.fromtimestamp(timestamp / division)

    @staticmethod
    def milliseconds_timestamp_to_dateime(timestamp):
        return TimeUtils.timestamp_to_dateime(timestamp, 1000.0)

    @staticmethod
    def unix_time_millis(dt):
        return int((dt - TimeUtils.EPOCH_MOMENT).total_seconds() * 1000.0)
    
    @staticmethod
    def get_time_stamp(dt, datetime_format=None):
        datetime_format = datetime_format if datetime_format else TimeUtils.DATETIME_FORMAT
        return dt.strftime(datetime_format)
