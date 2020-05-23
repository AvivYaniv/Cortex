
class ParsedSnapshotMessage:
    def __init__(self, user_info, snapshot_uuid, snapshot_timestamp, field, result, is_uri, metadata):
        self.user_info              =   user_info
        self.snapshot_uuid          =   snapshot_uuid
        self.snapshot_timestamp     =   snapshot_timestamp
        self.field                  =   field
        self.result                 =   result
        self.is_uri                 =   is_uri
        self.metadata               =   metadata
        