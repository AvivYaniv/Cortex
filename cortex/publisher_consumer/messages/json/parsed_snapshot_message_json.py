
from cortex.utils import json_to_object, object_to_json

from cortex.publisher_consumer.messages.parsed_snapshot_message import ParsedSnapshotMessage

class ParsedSnapshotMessageJson(ParsedSnapshotMessage):
    def serialize(self):
        return object_to_json(self)
        
    @staticmethod
    def deserialize(data):
        return json_to_object(data)
