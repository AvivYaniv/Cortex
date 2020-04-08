
import json
from collections import namedtuple

def object_to_json(o):
    return json.dumps(vars(o))
        
def json_to_object(data):
    return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
