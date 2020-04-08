
from cortex.publisher_consumer.messages.json import JsonMessage
from cortex.publisher_consumer.messages.raw_snapshot_message import RawSnapshotMessage

class RawSnapshotMessageJson(RawSnapshotMessage, JsonMessage):
    @staticmethod
    def deserialize(data):
        return JsonMessage.deserialize(data, RawSnapshotMessage)
        