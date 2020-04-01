from datetime import datetime

class HelloMessage:   
    def __init__(self, user_id, username, birth_date, gender):
        self.user_id        = user_id
        self.username       = username
        self.birth_date     = birth_date if isinstance(birth_date, datetime) else datetime.fromtimestamp(birth_date)
        self.gender         = gender
         
    def __repr__(self):
        return f'HelloMessage(user_id={self.user_id}, username={self.username}, birth_date={datetime.strftime(self.birth_date, HelloMessage.DATETIME_FORMAT)}, gender={self.gender})'
    
    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {datetime.strftime(self.birth_date, HelloMessage.CONCISE_DATE_FORMAT)} ({HelloMessage.GENDER_TABLE[self.gender]})'
    