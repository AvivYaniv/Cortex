from cortex.utils import object_to_json

def user_feelings_parser(snapshot):
    return object_to_json(snapshot.user_feeling)

user_feelings_parser.field      = 'user_feelings'
user_feelings_parser.extension  = '.json'
