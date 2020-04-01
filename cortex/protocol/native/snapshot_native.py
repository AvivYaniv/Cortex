import io

from cortex.sample import Snapshot

from cortex.sample import ColorImage
from cortex.sample import DepthImage

from ..snapshot import SnapshotMessage

class SnapshotMessageNative(SnapshotMessage):
    def serialize(self):
        return self.snapshot.serialize()
    
    @staticmethod
    def read(data):
        return Snapshot.read(io.BytesIO(data))
    