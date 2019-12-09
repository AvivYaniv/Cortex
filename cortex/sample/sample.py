from .userinformation import UserInformation
from .snapshot import Snapshot

class Sample:
    def __init__(self, user_information, snapshots):
        self.user_information = user_information
        self.snapshots        = snapshots
         
    def __repr__(self):
        return f'Sample(' + self.user_information.__repr__() + ', Snapshots=' + len(self.snapshots) + ')'
    
    def serialize(self):
        serialized = self.user_information.serialize()
        
        for snapshot in self.snapshots:
            serialized += snapshot.serialize()
        
        return serialized
    
    @staticmethod
    def deserialize(*, stream):
        user_information    = UserInformation.deserialize(stream=stream)
        yield user_information
        
        while True:
            try:
                snapshot    = Snapshot.deserialize(stream=stream)
                yield snapshot
            except EOFError:
                stream.close()
                break 
    