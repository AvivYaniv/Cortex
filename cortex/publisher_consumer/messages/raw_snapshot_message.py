
class RawSnapshotMessage:
    def __init__(self, user_info, snapshot_uuid, raw_snapshot_path):
        self.user_info          =   user_info
        self.snapshot_uuid      =   snapshot_uuid
        self.raw_snapshot_path  =   raw_snapshot_path
        