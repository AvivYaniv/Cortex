
from cortex.publisher_consumer.messages.json import JsonMessage
from cortex.publisher_consumer.messages.parsed_snapshot_message import ParsedSnapshotMessage

class ParsedSnapshotMessageJson(ParsedSnapshotMessage, JsonMessage):
    @staticmethod
    def deserialize(data):
        return JsonMessage.deserialize(data, ParsedSnapshotMessageJson)
