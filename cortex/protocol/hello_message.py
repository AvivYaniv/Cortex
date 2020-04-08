from datetime import datetime

from cortex.utils import TimeUtils

class HelloMessage:   
    GENDER_TABLE            = { 'm' : 'MALE' , 'f' : 'FEMALE', 'o' : 'OTHER' }
    
    def __init__(self, user_info):
        self.user_info      = user_info
    
    def __repr__(self):
        return f'HelloMessage(user_id={self.user_info.user_id}, username={self.user_info.username}, birth_date={datetime.strftime(self.user_info.birth_date, TimeUtils.DATETIME_FORMAT)}, gender={self.user_info.gender})'
    
    def __str__(self):
        return f'user {self.user_info.user_id}: {self.user_info.username}, born {datetime.strftime(self.user_info.birth_date, TimeUtils.CONCISE_DATE_FORMAT)} ({HelloMessage.GENDER_TABLE[self.user_info.gender]})'
    