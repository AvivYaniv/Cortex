
class ParsedSnapshotMessage:
    def __init__(self, user_id, usr_info_path, snapshot_uuid, field, result):
        self.user_id        =    user_id
        self.usr_info_path  = usr_info_path
        self.snapshot_uuid  =    snapshot_uuid
        self.field          =    field
        self.result         =    result
        