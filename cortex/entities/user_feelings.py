
class UserFeelings:
    def __init__(self, user_feeling):
        self.hunger, self.thirst, self.exhaustion, self.happiness = user_feeling

    def clear(self):
        self.hunger, self.thirst, self.exhaustion, self.happiness = (0.0, 0.0, 0.0, 0.0) 

    def get(self):
        return self.hunger, self.thirst, self.exhaustion, self.happiness
