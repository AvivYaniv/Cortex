
class ParsedSnapshotMessage:
    def __init__(self, user_id, snapshot_uuid, field, result):
        self.user_id        =    user_id
        self.snapshot_uuid  =    snapshot_uuid
        self.field          =    field
        self.result         =    result
        