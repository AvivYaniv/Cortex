from cortex.utils import object_to_json

def user_feelings_parser(parser_saver, context, snapshot):
    result = object_to_json(snapshot.user_feeling)
    return result
    
user_feelings_parser.field      = 'user_feelings'
user_feelings_parser.extension  = '.json'
