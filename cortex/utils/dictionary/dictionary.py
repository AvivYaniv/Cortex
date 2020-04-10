
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
