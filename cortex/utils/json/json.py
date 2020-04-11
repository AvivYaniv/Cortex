
import json
import datetime

from cortex.utils.dictionary import dictionary_to_object

def args_to_json(*args):
    return json.dumps(args)

def kwargs_to_json(**kwargs):
    return json.dumps(kwargs)

def object_to_json(o):
    return json.dumps(o, default=lambda x: x.__dict__)

def json_with_dates_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def dictionary_to_json(dictionary):
    return json.dumps(dictionary, default = json_with_dates_converter)
        
def json_to_object(data, _cls = None):
    converted = dictionary_to_object(json.loads(data))
    if _cls:
        converted.__class__ = _cls
    return converted     
