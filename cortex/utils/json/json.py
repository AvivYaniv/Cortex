
import json
from collections import namedtuple

from cortex.utils.dictionary import dictionary_to_object

def args_to_json(*args):
    return json.dumps(args)

def kwargs_to_json(**kwargs):
    return json.dumps(kwargs)

def object_to_json(o):
    return json.dumps(o, default=lambda x: x.__dict__)
        
def json_to_object(data, _cls = None):
    # TODO DEBUG REVISE
    # converted = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    converted = dictionary_to_object(json.loads(data))
    if _cls:
        converted.__class__ = _cls
    return converted     
