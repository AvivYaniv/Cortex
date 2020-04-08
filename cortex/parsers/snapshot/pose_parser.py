from cortex.utils import object_to_json

def pose_parser(parser_saver, context, snapshot):
    result = object_to_json(snapshot.pose)
    return result
    
pose_parser.field      = 'pose'
pose_parser.extension  = '.json'
