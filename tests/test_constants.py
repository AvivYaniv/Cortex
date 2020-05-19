
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
MESSAGE_QUEUE_TEST_HOST                 =   '0.0.0.0'

# Tests Folder
TESTS_FOLDER                            =   'tests'

# File Version
DEFAULT_FILE_VERSION                    =   ReaderVersions.PROTOBUFF 

# File names
EXAMPLE_FILE_PATH_FORMAT                =   'example%s.mind.gz'

# Raw Snapshot
RAW_SNAPSHOT_FOLDER                     =   '_snapshot'
RAW_SNAPSHOT_FILE_NAME                  =   'snapshot.raw'

# Parser Results Extension
PARSER_RESULT_FILE_EXTENSTION           =   '.result'

# Integration Folder
INTEGRATION_FOLDER                      =   '_integration'

# Publisher Consumer Folder
PUBLISHER_CONSUMER_FOLDER               =   'publisher_consumer'

# Saver Folder
SAVER_FOLDER                            =   'saver' 

# Saver Message Queue Messages Folder
SAVER_MESSAGE_QUEUE_MESSAGES_FOLDER     =   'saver_messages'

# Services
PARSER_SERVICE_TYPE                     =   'parser'
SAVER_SERVICE_TYPE                      =   'saver'

# Service Output Extension
SERVICE_OUTPUT_EXTENSTION               =   '.service_output'

# Message Queue Message Extension
MESSAGE_QUEUE_MESSAGE_EXTENSTION        =   '.message'

# Message Queue Messages Folder
MESSAGE_QUEUE_SERVICES_OUTPUTS_FOLDER   =   'services_outputs'

# Message Queue
SERVER_MESSAGES_IDS                     =   [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10' ]
SAVER_MOCK_DEFAULT_IDS                  =   [ '1', '2' ]
PARSER_TYPES                            =   [ 'pose', 'user_feelings', 'color_image', 'depth_image' ]
MESSAGE_QUEUE_TYPE                      =   None
DEFAULT_PROCCESS_DURATION               =   1
DEFAULT_JOIN_DURATION                   =   2
DEFAULT_INITIALIZATION_DURATION         =   5
DEFAULT_SHUTDOWN_DURATION               =   5

# CI/CD
CI_CD_TEST_ENVIRONMENT                  =   'TRAVIS'

def project_root():
    return str(pathlib.Path(abspath(getsourcefile(lambda:0))).parent.parent)

def get_user_test_file_path(test_user_number):
    return str(pathlib.Path(project_root(), EXAMPLE_FILE_PATH_FORMAT % test_user_number))

def get_raw_snapshot_file_path():
    return str(pathlib.Path(project_root(), TESTS_FOLDER, RAW_SNAPSHOT_FOLDER, RAW_SNAPSHOT_FILE_NAME))

def get_message_queue_serivce_outputs_path():
    return str(pathlib.Path(project_root(), TESTS_FOLDER, PUBLISHER_CONSUMER_FOLDER, MESSAGE_QUEUE_SERVICES_OUTPUTS_FOLDER))    

def get_message_queue_serivce_outputs_file_path(service_name):
    return str(pathlib.Path(get_message_queue_serivce_outputs_path(), service_name + SERVICE_OUTPUT_EXTENSTION))

def get_saver_message_queue_mesages_path():
    return str(pathlib.Path(project_root(), TESTS_FOLDER, SAVER_FOLDER, SAVER_MESSAGE_QUEUE_MESSAGES_FOLDER))    

def get_saver_message_queue_mesages_file_path(sender_name):
    return str(pathlib.Path(get_saver_message_queue_mesages_path(), sender_name + MESSAGE_QUEUE_MESSAGE_EXTENSTION))

def get_snapshot_result_file_name(parser_type):
    return parser_type + PARSER_RESULT_FILE_EXTENSTION

def get_raw_snapshot_result_path(parser_type):
    return str(pathlib.Path(project_root(), TESTS_FOLDER, RAW_SNAPSHOT_FOLDER, get_snapshot_result_file_name(parser_type)))
