
class RawSnapshotMessage:
    def __init__(self, user_id, snapshot_uuid, raw_snapshot_path):
        self.user_id            =   user_id
        self.snapshot_uuid      =   snapshot_uuid
        self.raw_snapshot_path  =   raw_snapshot_path
