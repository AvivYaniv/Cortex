from cortex.utils import object_to_json

def user_feelings_parser(parser_saver, context, snapshot, path=None):
    result = object_to_json(snapshot.user_feeling)
    if path:
        parser_saver.save_file(path, result)
    return result
    
user_feelings_parser.field      = 'user_feelings'
user_feelings_parser.extension  = '.json'
