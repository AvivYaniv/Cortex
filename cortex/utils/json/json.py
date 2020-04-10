
import json
from collections import namedtuple

def args_to_json(*args):
    return json.dumps(args)

def kwargs_to_json(**kwargs):
    return json.dumps(kwargs)

def object_to_json(o):
    return json.dumps(vars(o))
        
def json_to_object(data, _cls = None):
    converted = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if _cls:
        converted.__class__ = _cls
    return converted     
