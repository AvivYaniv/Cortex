
from cortex.utils import embed_dictionary_in_string

# API host
# Constants Section
DEFAULT_API_HOST                            =           '127.0.0.1'
DEFAULT_API_PORT                            =           '5000'
DEFAULT_API_HOSTNAME                        =           f'http://{DEFAULT_API_HOST}:{DEFAULT_API_PORT}'

# API prefix
API_VERSION                                 =           'v1.0'
API_PREFIX                                  =           f'/api/{API_VERSION}/'

# API URLs
API_URL_FORMAT_GET_ALL_USERS                =           f'users'                                                           
API_URL_FORMAT_GET_USER                     =           f'users/%user_id%'                                                 
# Snapshot API Section
API_URL_FORMAT_GET_ALL_USER_SNAPSHOTS       =           f'users/%user_id%/snapshots'                          
API_URL_FORMAT_GET_USER_SNAPSHOT            =           f'users/%user_id%/snapshots/%snapshot_uuid%'     
# Result API Section
API_URL_FORMAT_GET_RESULT                   =           f'users/%user_id%/snapshots/%snapshot_uuid%/%result_name%'
API_URL_FORMAT_GET_RESULT_DATA              =           f'users/%user_id%/snapshots/%snapshot_uuid%/%result_name%/data'
# Snapshot results API Section
API_URL_FORMAT_GET_SNAPSHOT_RESULTS         =           f'users/%user_id%/snapshots/%snapshot_uuid%/results'
API_URL_FORMAT_GET_ALL_USER_RESULTS         =           f'users/%user_id%/results'

# Embedding Dictionaries Section
DICT_ARGUNETS = {                                               \
                  '%user_id%'       : '{}',                     \
                  '%snapshot_uuid%' : '{}',                     \
                  '%result_name%'   : '{}',                     \
                }

# Methods Section
def get_custom_api_url(api_url_format, dictionary, host=''):
    return host + API_PREFIX + embed_dictionary_in_string(api_url_format, dictionary)

def get_api_url(api_url_format, host=None):
    host = host if host else DEFAULT_API_HOSTNAME
    return get_custom_api_url(api_url_format, DICT_ARGUNETS, host)
