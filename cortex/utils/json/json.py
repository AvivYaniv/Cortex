
import json
from collections import namedtuple

def object_to_json(o):
    return json.dumps(vars(o))
        
def json_to_object(data, _cls = None):
    converted = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if _cls:
        converted.__class__ = _cls
    return converted     
