
def strip_dictionary_fields_blacklist(dictionary, disapproved_keys):
    if dictionary:
        for key in disapproved_keys: dictionary.pop(key, None)    

def strip_dictionary_fields_whitelist(dictionary, approved_keys):
    if dictionary:            
        disapproved_keys = [k for k in dictionary if k not in approved_keys]
        strip_dictionary_fields_blacklist(dictionary, disapproved_keys)    

def object_to_dictionary(o):
    return vars(o)

class dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, dict2obj(b) if isinstance(b, dict) else b)

def dictionary_to_object(d, cls = None):
    converted = dict2obj(d)
    if cls:
        converted.__class__ = cls
    return converted 

def embed_dictionary_in_string(raw_string, dictionary):
    embedded_string = raw_string
    for key, value in dictionary.items():
        embedded_string = embedded_string.replace(key, value)
    return embedded_string
