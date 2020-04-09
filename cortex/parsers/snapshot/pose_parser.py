from cortex.utils import object_to_json

def pose_parser(snapshot):
    return object_to_json(snapshot.pose)

pose_parser.field      = 'pose'
pose_parser.extension  = '.json'
