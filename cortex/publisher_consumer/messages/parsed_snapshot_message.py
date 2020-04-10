
class ParsedSnapshotMessage:
    def __init__(self, user_info, snapshot_uuid, field, result, is_uri):
        self.user_info      =   user_info
        self.snapshot_uuid  =   snapshot_uuid
        self.field          =   field
        self.result         =   result
        self.is_uri         =   is_uri
        