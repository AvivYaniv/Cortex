
from furl import furl

def parse_url(url_str):
    f = furl(url_str)
    protocol, host, port = \
        f._scheme, f._host, f._port
    return protocol, host, port
