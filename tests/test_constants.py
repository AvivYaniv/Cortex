
import pathlib
from inspect import getsourcefile
from os.path import abspath

from cortex.readers.reader_versions import ReaderVersions

# User Section
TEST_USER_1_ID                          =   '42'
TEST_USER_2_ID                          =   '100'

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

def get_user_test_file_path(user_id):
    return str(pathlib.Path(project_root(), EXAMPLE_FILE_PATH_FORMAT % user_id))
