from cortex.utils import object_to_json

def pose_parser(parser_saver, context, snapshot, path=None):
    result = object_to_json(snapshot.pose)
    if path:
        parser_saver.save_file(path, result)
    return result
    
pose_parser.field      = 'pose'
pose_parser.extension  = '.json'
