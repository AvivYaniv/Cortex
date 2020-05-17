
import pathlib
from inspect import getsourcefile
from os.path import abspath

from cortex.readers.reader_versions import ReaderVersions

# User Section
class TEST_USER_1:
    ID                          =   '42'
    NAME                        =   'Dan Gittik'
    
class TEST_USER_2:
    ID                          =   '100'
    NAME                        =   'Test User'

TEST_USERS_ARRAY                =   [ TEST_USER_1(), TEST_USER_2() ]

def get_test_user(number):
    index = number - 1
    if len(TEST_USERS_ARRAY) <= index:
        raise NotImplementedError(f'No test user {number}')
    return TEST_USERS_ARRAY[index]
    
# Durations Section
SERVER_SNAPSHOT_MAX_DURATION_HANDLING   =   2

# Hosts
SERVER_TEST_HOST                        =   '0.0.0.0'

# File Version
DEFAULT_FILE_VERSION                    =   ReaderVersions.PROTOBUFF 

# File names
EXAMPLE_FILE_PATH_FORMAT                =   'example%s.mind.gz'

def project_root():
    return str(pathlib.Path(abspath(getsourcefile(lambda:0))).parent.parent)

def get_user_test_file_path(test_user_number):
    return str(pathlib.Path(project_root(), EXAMPLE_FILE_PATH_FORMAT % test_user_number))
