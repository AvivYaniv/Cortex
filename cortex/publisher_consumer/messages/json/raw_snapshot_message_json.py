
from cortex.utils import json_to_object, object_to_json

from cortex.publisher_consumer.messages.raw_snapshot_message import RawSnapshotMessage

class RawSnapshotMessageJson(RawSnapshotMessage):
    def serialize(self):
        return object_to_json(self)
        
    @staticmethod
    def deserialize(data):
        return json_to_object(data)
        